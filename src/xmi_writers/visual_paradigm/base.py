import xml.etree.ElementTree as xml
import enum

@enum.unique
class MessageSort(enum.Enum):
    synchCall = 0,
    asyncCall = 1,
    reply = 2

def init_root():
    return xml.Element('xmi:XMI', {
        'xmi:version': '2.1',
        'xmlns:xmi': "https://www.omg.org/spec/XMI/2.1.1",
        'xmlns:uml': "http://www.eclipse.org/uml2/2.0.0/UML",
        # 'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance"
    })


# Model section
def create_subelement(parent: xml.Element, tag_name: str, attr: dict[str, str]):
    return xml.SubElement(parent, tag_name, attr)

def create_model(parent, id: str, name: str):
    return create_subelement(parent, 'uml:Model', {
        'xmi:id': id,
        # 'xmi:type': 'uml:Model',
        'name': name
    })

def create_packagedElement(parent: xml.Element, id: str, uml_type: str, name: str = ''):
    return create_subelement(parent, 'packagedElement', {
        'xmi:id': id,
        'xmi:type': uml_type,
        'name': name
    })

def create_ownedBehavior(parent: xml.Element, id, name: str = 'Sequence Diagram1'):
    return create_subelement(parent, 'ownedBehavior', {
        'xmi:id': id,
        'xmi:type': 'uml:Interaction',
        'name': name
    })

def create_lifeline(parent: xml.Element, id: str, covered_by: str, name: str = 'Object'):
    return create_subelement(parent, 'lifeline', {
        'xmi:id': id,
        'xmi:type': 'uml:Lifeline',
        'name': name,
        'coveredBy': covered_by
    })

def create_message(parent: xml.Element, id: str, message_sort: MessageSort, name: str, receive_event, send_event):
    return create_subelement(parent, 'message', {
        'xmi:id': id,
        'xmi:type': 'uml:Message',
        'messageSort': message_sort.name,
        'name': name,
        'receiveEvent': receive_event,
        'sendEvent': send_event
    })

def create_ownedComment(parent: xml.Element, id: str, name: str = '', body: str = ''):
    return create_subelement(parent, 'ownedComment', {
        'xmi:id': id,
        'xmi:type': 'uml:Comment',
        'name': name,
        'body': body
    })

def create_fragment(parent: xml.Element, id: str, covered: str, message: str):
    return create_subelement(parent, 'fragment', {
        'xmi:id': id,
        'xmi:type': 'uml:MessageOccurrenceSpecification',
        'event': 'defaultEventOfMessageOccurrency',
        'covered': covered,
        'message': message
    })

def create_CombinedFragment(parent: xml.Element, id: str, interaction_operator: str, covered: str, uml_type: str = 'uml:CombinedFragment', name: str = 'CombinedFragment'):
    return create_subelement(parent, 'fragment', {
        'xmi:id': id,
        'xmi:type': uml_type,
        'name': name,
        'interactionOperator': interaction_operator,
        'covered': covered
    })

def create_operand(parent: xml.Element, id: str, covered: str, name: str = 'Operand', uml_type: str = 'uml:InteractionOperand'):
    return create_subelement(parent, 'operand', {
        'xmi:id': id,
        'xmi:type': uml_type,
        'name': name,
        'covered': covered
    })

def create_actor(parent, id: str, name: str):
    return create_subelement(parent, 'packagedElement', {
        'xmi:id': id,
        'xmi:type': 'uml:Actor',
        'name': name
    })

def create_interaction(parent: xml.Element):
    return create_subelement(parent, 'packagedElement', {
        'xsi:type': 'uml:Interaction',
        'xmi:id': 'id',
        'name': 'name'
    })


# Diagram section
def create_DiagramElement(parent: xml.Element,
                          preferredShapeType: str,
                          subject: str,
                          geometry: str,
                          id: str,
                          fromDiagramElement: str = '',
                          toDiagramElement: str = ''):
    attr = { 'id': id }
    if preferredShapeType:
        attr['preferredShapeType'] = preferredShapeType
    if subject:
        attr['subject'] = subject
    if geometry:
        attr['geometry'] = geometry
    if fromDiagramElement:
        attr['fromDiagramElement'] = fromDiagramElement
    if toDiagramElement:
        attr['toDiagramElement'] = toDiagramElement

    return create_subelement(parent, 'uml:DiagramElement', attr)

def create_elementFill(parent: xml.Element,
                       style: str = '1',
                       transparency: str = '0',
                       type: str = '1',
                       color1: str = 'Cr:122,207,245,255',
                       color2: str = ''):
    attr = {
        'style': style,
        'transparency': transparency,
        'type': type,
        'color1': color1,
        'color2': color2
    }
    return create_subelement(parent, 'elementFill', attr)

def create_elementFont(parent: xml.Element,
                       bold: str = 'false',
                       color: str = 'Cr:0,0,0,255',
                       italic: str = 'false',
                       style: str = '0',
                       name: str = 'Dialog',
                       size: str = '11'):
    attr = {
        'color': color,
        'bold': bold,
        'italic': italic,
        'style': style,
        'name': name,
        'size': size
    }
    return create_subelement(parent, 'elementFont', attr)

def create_elementLine(parent: xml.Element,
                       color: str = 'Cr:0,0,0,255',
                       style: str = '1',
                       transparency: str = '0',
                       weight: str = '1.0'):
    attr = {
        'color': color,
        'style': style,
        'transparency': transparency,
        'weight': weight
    }
    return create_subelement(parent, 'elementFont', attr)

def create_Diagram(parent: xml.Element, id: str, diagramType: str, documentation: str = '', name: str = 'Sequence Diagram1'):
    attr = {
        'xmi:id': id,
        'diagramType': diagramType,
        'documentation': documentation
    }
    return create_subelement(parent, 'uml:Diagram', attr)

def create_Diagram_element(parent: xml.Element):
    return create_subelement(parent, 'uml:Diagram.element', {})