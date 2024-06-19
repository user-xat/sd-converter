import uuid
import logging
import numpy as np
from pydantic import BaseModel, Field, ConfigDict
import model.elements as elems
from model.wrapper import SDWrappedElement
from model.object_types import ObjectType


class SDModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    orig_img: np.ndarray = Field(exclude=True)
    elements: list[SDWrappedElement] = Field(exclude=True)
    root: SDWrappedElement = Field(default_factory=lambda: SDWrappedElement(this=None), init=False)
    objects: list[elems.SDObject] = Field(default_factory=list, init=False, exclude=True)
    messages: list[elems.SDMessage] = Field(default_factory=list, init=False, exclude=True)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, init=False)
    diagram_id: uuid.UUID = Field(default_factory=uuid.uuid4, init=False)

    def __init_mess_obj(self):
        self.objects = [elem.this for elem in self.elements if elem.this.is_object()]
        self.objects.sort(key= lambda obj: obj.xyxy[0])
        self.messages = [elem.this for elem in self.elements if elem.this.is_message()]
        self.messages.sort(key=lambda mes: mes.xyxy[1])

    @classmethod
    def make(cls, data, coef) -> "SDModel":
        logging.info(f'creating a model for the {data.path}')
        model: list[SDWrappedElement] = list()
        for box in data.boxes:
            cls = ObjectType(box.cls.item())
            conf = box.conf.item()
            xyxy = np.round(box.xyxy.numpy()[0]).astype(int)
            xyxyn = box.xyxyn.numpy()[0]
            if cls == ObjectType.package:
                sd_elem = elems.SDPackage(cls=cls, conf=conf, xyxy=xyxy, xyxyn=xyxyn)
            elif cls in [ObjectType.actor, ObjectType.object, ObjectType.database]:
                sd_elem = elems.SDObject(cls=cls, conf=conf, xyxy=xyxy, xyxyn=xyxyn)
            elif cls in [ObjectType.synchronous_message,
                         ObjectType.asynchronous_message,
                         ObjectType.reply_message,
                         ObjectType.recursive_sync_message,
                         ObjectType.recursive_reply_message]:
                sd_elem = elems.SDMessage(cls=cls, conf=conf, xyxy=xyxy, xyxyn=xyxyn)
            elif cls == ObjectType.note:
                sd_elem = elems.SDNote(cls=cls, conf=conf, xyxy=xyxy, xyxyn=xyxyn)
            else:
                sd_elem = elems.SDElement(cls=cls, conf=conf, xyxy=xyxy, xyxyn=xyxyn)
            model.append(SDWrappedElement(this=sd_elem, coef=coef))
        logging.debug(f'elements = {len(model)}')
        return SDModel(elements=model, orig_img=data.orig_img)

    def create_model(self) -> None:
        logging.info('the process of creating links between the elements has started')
        self.__init_mess_obj()
        self.__create_links()
        self.__find_pair_message()
        self.__find_sub_elements()
        self.__align_objects_size()

    def items(self):
        return self.root.items()

    # Create links between objects and messages
    def __create_links(self):
        logging.info('creating links between objects and messages')
        for message in self.messages:
            x1, _, x2, _ = message.xyxy
            left_obj, right_obj = None, None
            for obj in self.objects:
                if obj.contain_point_x(x1):
                    left_obj = obj
                elif obj.contain_point_x(x2):
                    right_obj = obj
                if left_obj and right_obj:
                    break

            left_connect = elems.ObjMesConnection(obj=left_obj, message=message) if left_obj else None
            right_connect = elems.ObjMesConnection(obj=right_obj, message=message) if right_obj else None
            if message.cls == ObjectType.reply_message:
                message.sender = right_connect
                message.receiver = left_connect
                if left_obj:
                    left_obj.receive_messages.append(left_connect)
                if right_obj:
                    right_obj.send_messages.append(right_connect)
            elif message.cls in [ObjectType.recursive_sync_message, ObjectType.recursive_reply_message]:
                # нельзя переиспользовать left_connect. Нужен новый объект
                left2 = elems.ObjMesConnection(obj=left_obj, message=message) if left_obj else None
                message.sender = left_connect
                message.receiver = left2
                if left_obj:
                    left_obj.send_messages.append(left_connect)
                    left_obj.receive_messages.append(left2)
            else:
                message.sender = left_connect
                message.receiver = right_connect
                if left_obj:
                    left_obj.send_messages.append(left_connect)
                if right_obj:
                    right_obj.receive_messages.append(right_connect)

    def __find_pair_message(self):
        logging.info('searching for message pairs')
        for i, send in enumerate(self.messages):
            if send.cls not in [ObjectType.synchronous_message,
                                 ObjectType.asynchronous_message,
                                 ObjectType.recursive_sync_message]:
                continue

            reply_mes: elems.SDMessage = None
            for j in range(i+1, len(self.messages)):
                receive = self.messages[j]
                if send.sender and receive.receiver and send.receiver and receive.sender\
                     and send.sender.obj != receive.receiver.obj and send.receiver.obj != receive.sender.obj:
                    continue
                if send.cls in [ObjectType.synchronous_message, ObjectType.asynchronous_message]\
                    and receive.cls == ObjectType.reply_message:
                    reply_mes = receive
                elif send.cls == ObjectType.recursive_sync_message and receive.cls == ObjectType.recursive_reply_message:
                    reply_mes = receive
                break

            send.pair = reply_mes
            if reply_mes:
                reply_mes.pair = send

    def __align_objects_size(self):
        max_y: int = 0
        for elem in self.items():
            max_y = max(elem.xyxy[3], max_y)
        
        for obj in self.objects:
            if not obj.terminator:
                obj.xyxy = (obj.xyxy[0], obj.xyxy[1], obj.xyxy[2], max_y)
    
    def __find_sub_elements(self):
        logging.info('determining the nesting of elements')
        self.root.sub_elements.extend(self.elements)
        self.root.find_sub_elements()
        self.root.get_attributes(self.orig_img, self.objects)