from docx.oxml.text.paragraph import CT_P
from lxml.etree import ElementTree, _Element
from docxlatex import Document



def contains_mathml(element: CT_P):
    xml_str = element.xml
    return '<m:' in xml_str

def xml_to_text(element: CT_P):
    xml_str = element.xml
    xml_to_text = Document("").xml_to_text
    latex_text = xml_to_text(xml_str)
    return latex_text.replace('\n', '').replace(' ','')


def extract_toc_entries(xml_tree: _Element):
    root = ElementTree(xml_tree).getroot()
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    }

    toc_entries = []

    # Iterate over all paragraph elements
    for para in root.findall('.//w:p', namespaces):
        # Find the paragraph style
        para_style = para.find('w:pPr/w:pStyle', namespaces)
        if para_style is not None and para_style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '').startswith('TOC'):
            text_elements = para.findall('.//w:t', namespaces)
            toc_text = '\t\tPage '.join([t.text or '' for t in text_elements if t.text])
            if toc_text:  # Avoid adding empty entries
                toc_entries.append(toc_text)

    return '\n'.join(toc_entries)