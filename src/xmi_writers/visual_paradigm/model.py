import uuid
import xmi_writers.visual_paradigm.base as base
import xml.etree.ElementTree as xml
from model.model import SDModel
from model.elements import SDObject, SDMessage, SDNote, SDPackage, SDElement, ObjMesConnection
from model.object_types import ObjectType


MESSAGE_TYPE = {
    ObjectType.synchronous_message: base.MessageSort.synchCall,
    ObjectType.asynchronous_message: base.MessageSort.asyncCall,
    ObjectType.reply_message: base.MessageSort.reply,
    ObjectType.recursive_sync_message: base.MessageSort.synchCall,
    ObjectType.recursive_reply_message: base.MessageSort.reply,
}

def init_xmi():
    return base.init_root()

def create_model(parent:xml.Element, model: SDModel):
    model = base.create_model(parent, model.id.hex, 'sd_model')
    base.create_subelement(model, 'packagedElement', {
        'xmi:id': 'defaultEventOfMessageOccurrency',
        'xmi:type': 'uml:AnyReceiveEvent'
    })
    return model

def create_object(parent: xml.Element, elem: SDObject):
    sm = [conn.id.hex for conn in elem.send_messages]
    rm = [conn.id.hex for conn in elem.receive_messages]
    covered_by = ' '.join(sm + rm)

    lifeline = base.create_lifeline(parent, elem.id.hex, covered_by, elem.name)
    ext = base.create_subelement(lifeline, 'xmi:Extension', { "extender": "Visual Paradigm"})
    base.create_subelement(ext, "stopped", {"xmi:value": 'true' if elem.terminator else 'false'})

    return lifeline

def create_note(parent: xml.Element, elem: SDNote):
    return base.create_ownedComment(parent, elem.id.hex, elem.name, elem.body)

def create_package(parent: xml.Element, elem: SDPackage):
    return base.create_packagedElement(parent, elem.id.hex, 'uml:Package', elem.name)

def create_collaboration(parent: xml.Element):
    return base.create_subelement(parent, 'packagedElement', {
        'xmi:type': 'uml:Collaboration'
    })

def create_interaction(parent: xml.Element):
    return base.create_subelement(parent, 'ownedBehavior', {
        'xmi:id': uuid.uuid4().hex,
        'xmi:type': 'uml:Interaction',
        'name': 'Sequence Diagram1'
    })

def create_message(parent: xml.Element, elem: SDMessage):
    msg = base.create_message(parent, elem.id.hex, MESSAGE_TYPE[elem.cls], elem.name, elem.receiver.id.hex if elem.receiver else "", elem.sender.id.hex if elem.sender else "")
    if ObjectType.recursive_sync_message or ObjectType.recursive_reply_message:
        ext = base.create_subelement(msg, 'Extension', { "extender": "Visual Paradigm"})
        base.create_subelement(ext, 'type', {"xmi:value": "recursive"})

def create_fragment(parent: xml.Element, conn: ObjMesConnection):
    return base.create_fragment(parent, conn.id.hex if conn else "", conn.obj.id.hex if conn else "", conn.message.id.hex if conn else "")

def create_loop(parent: xml.Element, elem: SDElement):
    labels: list = elem.attr.get('labels', list())
    label: str = labels[0] if labels.count() > 0 else ''
    loop = base.create_fragment(parent, elem.id.hex, 'loop', label)
    return base.create_operand(loop, elem.id.hex, name='loop_operand', uml_type='uml:InteractionOperand')

def create_opt(parent: xml.Element, elem: SDElement):
    opt = base.create_fragment(parent, elem.id.hex, 'opt')
    return base.create_operand(opt, elem.id.hex, name='opt_operand')

def creaete_alt(parent: xml.Element, elem: SDElement):
    alt = base.create_fragment(parent, elem.id.hex, 'alt')
    return base.create_operand(alt, elem.id.hex, name='alt_operand')

def create_ref(parent: xml.Element, elem: SDElement):
    pass
