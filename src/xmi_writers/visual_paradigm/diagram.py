import xmi_writers.visual_paradigm.base as base
import xml.etree.ElementTree as xml
from model.elements import SDObject, SDNote, SDMessage
from model.model import SDModel


def create_Diagram(parent: xml.Element, model: SDModel):
    diagram = base.create_Diagram(parent,
                        id=model.diagram_id.hex,
                        diagramType='InteractionDiagram')
    return base.create_Diagram_element(diagram)

def create_object(parent: xml.Element, obj: SDObject):
    xml_obj = base.create_DiagramElement(parent,
                                         preferredShapeType='InteractionLifeLine',
                                         subject=obj.id.hex,
                                         geometry=obj.get_geometry(),
                                         id=obj.diagram_id.hex)
    base.create_elementFill(parent)
    base.create_elementFont(parent)
    base.create_elementLine(parent)
    return xml_obj

# <uml:DiagramElement geometry="545,40,70,164" preferredShapeType="InteractionLifeLine" subject="sBL9CPGGAqBwATS3" xmi:id="sBL9CPGGAqBwATS2">
#     <elementFill color1="Cr:122,207,245,255" color2="" style="1" transparency="0" type="1"/>
#     <elementFont bold="false" color="Cr:0,0,0,255" italic="false" name="Dialog" size="11" style="0"/>
#     <elementLine color="Cr:0,0,0,255" style="1" transparency="0" weight="1.0"/>
# </uml:DiagramElement>

def create_actor(parent: xml.Element, obj: SDObject):
    xml_actor = base.create_DiagramElement(parent,
                                           preferredShapeType='InteractionActor',
                                           subject=obj.id.hex,
                                           geometry=obj.get_geometry(),
                                           id=obj.diagram_id.hex)
    base.create_elementFill(xml_actor)
    base.create_elementFont(xml_actor)
    base.create_elementLine(xml_actor)
    return xml_actor

# <uml:DiagramElement geometry="165,40,60,164" preferredShapeType="InteractionActor" subject="t2z9CPGGAqBwATSu" xmi:id="N2z9CPGGAqBwATSt">
# 	<elementFill color1="Cr:122,207,245,255" color2="" style="1" transparency="0" type="1"/>
# 	<elementFont bold="false" color="Cr:0,0,0,255" italic="false" name="Dialog" size="11" style="0"/>
# 	<elementLine color="Cr:0,0,0,255" style="1" transparency="0" weight="1.0"/>
# </uml:DiagramElement>

def create_note(parent: xml.Element, note: SDNote):
    xml_note = base.create_DiagramElement(parent,
                                          preferredShapeType='NOTE',
                                          subject=note.id.hex,
                                          geometry=note.get_geometry(),
                                          id=note.diagram_id.hex)
    base.create_elementFill(xml_note)
    base.create_elementFont(xml_note)
    base.create_elementLine(xml_note)
    return xml_note

# <uml:DiagramElement geometry="259,26,251,40" preferredShapeType="NOTE" subject="VLuXCPGGAqBwAT1I" xmi:id="VLuXCPGGAqBwAT1H">
#     <elementFill color1="Cr:122,207,245,255" color2="" style="1" transparency="0" type="1"/>
#     <elementFont bold="false" color="Cr:0,0,0,255" italic="false" name="Dialog" size="12" style="0"/>
#     <elementLine color="Cr:0,0,0,255" style="1" transparency="0" weight="1.0"/>
# </uml:DiagramElement>

def create_message(parent: xml.Element, message: SDMessage):
    fromObj = message.sender.obj.diagram_id.hex if message.sender and message.sender.obj else ""
    toObj = message.receiver.obj.diagram_id.hex if message.receiver and message.receiver.obj else ""
    xml_message = base.create_DiagramElement(parent,
                                             preferredShapeType='Message',
                                             subject=message.id.hex,
                                             geometry=message.get_geometry(),
                                             id=message.diagram_id.hex,
                                             fromDiagramElement=fromObj,
                                             toDiagramElement=toObj)
    base.create_elementFont(xml_message)
    base.create_elementLine(xml_message)
    return xml_message

# <uml:DiagramElement fromDiagramElement="sBL9CPGGAqBwATS2" geometry="576,172;199,172;" preferredShapeType="Message" subject=".7UrCPGGAqBwATTi" toDiagramElement="N2z9CPGGAqBwATSt" xmi:id="h7UrCPGGAqBwATTl">
# 	<elementFont bold="false" color="Cr:0,0,0,255" italic="false" name="Dialog" size="11" style="0"/>
# 	<elementLine color="Cr:0,0,0,255" style="1" transparency="0" weight="1.0"/>
# </uml:DiagramElement>

def create_activation(parent: xml.Element):
    xml_activation = base.create_DiagramElement(parent,
                                                preferredShapeType='Activation',
                                                subject='',
                                                geometry='',
                                                id='')
    base.create_elementFill(xml_activation)
    base.create_elementFont(xml_activation)
    base.create_elementLine(xml_activation)
    return xml_activation

# <uml:DiagramElement geometry="576,142,8,42" preferredShapeType="Activation" subject="oK_LCPGGAqBwATTV" xmi:id="0K_LCPGGAqBwATTX">
# 	<elementFill color1="Cr:122,207,245,255" color2="" style="1" transparency="0" type="1"/>
# 	<elementFont bold="false" color="Cr:0,0,0,255" italic="false" name="Dialog" size="11" style="0"/>
# 	<elementLine color="Cr:0,0,0,255" style="1" transparency="0" weight="1.0"/>
# </uml:DiagramElement>