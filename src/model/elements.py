import uuid
from pydantic import BaseModel, Field
from typing import Union
from model.object_types import ObjectType

class SDElement(BaseModel):
    cls: ObjectType
    conf: float
    xyxy: tuple[int, int, int, int]
    xyxyn: tuple[float, float, float, float]
    # attr: dict[str, Any] = Field(default_factory=dict, init=False)
    name: str = Field(default_factory=str, init=False)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, init=False)
    diagram_id: uuid.UUID = Field(default_factory=uuid.uuid4, init=False)

    def get_height(self) -> int:
        return self.xyxy[3] - self.xyxy[1]
    
    def get_width(self) -> int:
        return self.xyxy[2] - self.xyxy[0]
    
    def get_x(self) -> int:
        return self.xyxy[0]
    
    def get_y(self) -> int:
        return self.xyxy[1]

    def get_geometry(self) -> str:
        return f"{self.get_x()},{self.get_y()},{self.get_width()},{self.get_height()}"

    def is_message(self) -> bool:
        return self.cls in [ObjectType.synchronous_message,
                            ObjectType.asynchronous_message,
                            ObjectType.reply_message,
                            ObjectType.recursive_sync_message,
                            ObjectType.recursive_reply_message]
    
    def is_object(self) -> bool:
        return self.cls in [ObjectType.actor,
                            ObjectType.database,
                            ObjectType.object]
    
    def has_text(self) -> bool:
        return self.cls in [ObjectType.actor,
                            ObjectType.database,
                            ObjectType.object,
                            ObjectType.note,
                            ObjectType.synchronous_message,
                            ObjectType.asynchronous_message,
                            ObjectType.reply_message,
                            ObjectType.recursive_sync_message,
                            ObjectType.recursive_reply_message]

    def __get_area(self) -> float:
        x1, y1, x2, y2 = self.xyxy
        assert x1 < x2 and y1 < y2
        return (x2-x1) * (y2-y1)
    
    def __get_cross_area(self, other: "SDElement") -> float:
        ax1 ,ay1, ax2, ay2 = self.xyxy     # прямоугольник А
        bx1, by1, bx2, by2 = other.xyxy    # прямоугольник B

        left = max(ax1, bx1)
        right = min(ax2, bx2)
        top = max(ay1, by1)
        bottom = min(ay2, by2)

        width = right - left
        height = bottom - top

        if width < 0 or height < 0:
            return 0
        return width * height

    def __is_cross(self, other: "SDElement") -> bool:
        ax1 ,ay1, ax2, ay2 = self.xyxy     # прямоугольник А
        bx1, by1, bx2, by2 = other.xyxy    # прямоугольник B

        xA, yA = [ax1, ax2], [ay1, ay2]
        xB, yB = [bx1, bx2], [by1, by2]
        # не пересекаются
        return not (max(xA) < min(xB) or min(xA) > max(xB) or max(yA) < min(yB) or min(yA) > max(yB))

    def contain_elem(self, other: "SDElement") -> bool:
        if not self.__is_cross(other):
            return False
        other_area: float = other.__get_area()
        cross_area: float = self.__get_cross_area(other)
        return cross_area / other_area

    def contain_point_x(self, x: float, delta: float = 10) -> bool:
        x1, _, x2, _ = self.xyxy
        x1, x2 = max(x1 - delta, 0), x2 + delta
        return x1 <= x <= x2
    
    def contain_section_x(self, elem: "SDElement", delta: float = 5) -> bool:
        x1 = max(self.xyxy[0] - delta, 0)
        x2 = self.xyxy[2] + delta
        return x1 <= elem.xyxy[0] and elem.xyxy[2] <= x2


class SDObject(SDElement):
    terminator: bool = Field(default=False, init=False)
    send_messages: list["ObjMesConnection"] = Field(default_factory=list, init=False)
    receive_messages: list["ObjMesConnection"] = Field(default_factory=list, init=False)


class SDMessage(SDElement):
    sender: Union["ObjMesConnection", None] = Field(default=None, init=False)
    receiver: Union["ObjMesConnection", None] = Field(default=None, init=False)
    pair: Union["SDMessage", None] = Field(default=None, init=False)

    def get_geometry(self) -> str:
        x2 = self.get_x() + self.get_width()
        if self.is_reply():
            return f"{x2},{self.get_y()};{self.get_x()},{self.get_y()};"
        return f"{self.get_x()},{self.get_y()};{x2},{self.get_y()};"

    def is_async(self) -> bool:
        return self.cls == ObjectType.asynchronous_message
    
    def is_reply(self) -> bool:
        return self.cls == ObjectType.reply_message or self.cls == ObjectType.recursive_reply_message


class ObjMesConnection(BaseModel):
    obj: SDObject
    message: SDMessage
    id: uuid.UUID = Field(default_factory=uuid.uuid4, init=False)


class SDNote(SDElement):
    body: str = Field(default_factory=str, init=False)


class SDPackage(SDElement):
    pass