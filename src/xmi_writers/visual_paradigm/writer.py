import xmi_writers.visual_paradigm.model as xmi_model
import xmi_writers.visual_paradigm.diagram as xmi_diagram
import xml.etree.ElementTree as xml
from model.model import SDModel
from model.wrapper import SDWrappedElement
from model.elements import SDPackage, SDNote, SDObject, SDMessage
from model.object_types import ObjectType


def write(filename: str, sd_model: SDModel):
    xml_root = xmi_model.init_xmi()
    _write_model(xml_root, sd_model)
    _write_diagram(xml_root, sd_model)
    tree = xml.ElementTree(xml_root)
    xml.indent(tree, space='  ')
    tree.write(filename, encoding='utf-8', xml_declaration=True)

# Model
def _write_model(root: xml.Element, model: SDModel):
    xml_model = _create_model(root, model)
    xml_model = xmi_model.create_collaboration(xml_model)
    xml_model = xmi_model.create_interaction(xml_model)
    _sub_write_model(xml_model, model.root)

def _sub_write_model(root: xml.Element, sd_elem: SDWrappedElement):
    # if sd_elem.this and root.tag == 'uml:Model' and not isinstance(sd_elem.this, SDPackage):
    #     root = model.create_collaboration(root)
    #     root = model.create_interaction(root)

    xml_elem = root
    if sd_elem.this:
        if isinstance(sd_elem.this, SDPackage):
            xml_elem = _create_package(root, sd_elem.this)
        elif isinstance(sd_elem.this, SDNote):
            xml_elem = _create_note(root, sd_elem.this)
        elif isinstance(sd_elem.this, SDObject):
            xml_elem = _create_object(root, sd_elem.this)
        elif isinstance(sd_elem.this, SDMessage):
            xml_elem = _create_message(root, sd_elem.this)

    [_sub_write_model(xml_elem, sub_sd_elem) for sub_sd_elem in sd_elem.sub_elements]

def _create_model(parent: xml.Element, sd_model: SDModel):
    return xmi_model.create_model(parent, sd_model)

def _create_object(parent: xml.Element, obj: SDObject):
    return xmi_model.create_object(parent, obj)

def _create_message(parent: xml.Element, message: SDMessage) -> None:
    mes = xmi_model.create_message(parent, message)
    xmi_model.create_fragment(parent, message.sender)
    xmi_model.create_fragment(parent, message.receiver)
    return mes

def _create_package(parent: xml.Element, package: SDPackage):
    xml_pkg = xmi_model.create_package(parent, package)
    return xmi_model.create_interaction(xml_pkg)

def _create_note(parent: xml.Element, note: SDNote):
    return xmi_model.create_note(parent, note)

# Diagram
def _write_diagram(root: xml.Element, model: SDModel):
    xml_diagram = xmi_diagram.create_Diagram(root, model)
    _sub_write_diagram(xml_diagram, model.root)

def _sub_write_diagram(root: xml.Element, sd_elem: SDWrappedElement):
    xml_elem = root
    if sd_elem.this:
        if isinstance(sd_elem.this, SDNote):
            xml_elem = _create_note_diagram(root, sd_elem.this)
        elif isinstance(sd_elem.this, SDObject):
            xml_elem = _create_object_diagram(root, sd_elem.this)
        elif isinstance(sd_elem.this, SDMessage):
            xml_elem = _create_message_diagram(root, sd_elem.this)
    
    [_sub_write_diagram(xml_elem, sub_sd_elem) for sub_sd_elem in sd_elem.sub_elements]

def _create_note_diagram(parent: xml.Element, note: SDNote):
    return xmi_diagram.create_note(parent, note)

def _create_object_diagram(parent: xml.Element, obj: SDObject):
    if obj.cls == ObjectType.actor:
        return xmi_diagram.create_actor(parent, obj)
    else:
        return xmi_diagram.create_object(parent, obj)

def _create_message_diagram(parent: xml.Element, message: SDMessage):
    return xmi_diagram.create_message(parent, message)