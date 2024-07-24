from docx.oxml.text.paragraph import CT_P
from lxml.etree import ElementTree, _Element
from docxlatex import Document
from docx.table import Table
from io import StringIO
import docx.document



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


def table_to_plain_text(table: Table):
    output = StringIO()

    # Process the cells to handle MathML and convert them to plain text
    for row in table.rows:
        row_text = []
        for cell in row.cells:
            if contains_mathml(cell._element):  # Assuming this function exists
                cell.text = xml_to_text(cell._element)  # Assuming this function exists
            row_text.append(cell.text)
        # Skip the row if all elements are empty strings
        if all(cell_text == '' for cell_text in row_text):
            continue
        # Join the cell texts with commas and add a newline at the end
        output.write("[ " +" | ".join(row_text) + " ]" + "\n")

    return output.getvalue()


def create_element_index_dict(doc: docx.document.Document):
    body_element = doc._body._element

    PARAGRAPH_TAG = 'p'
    TABLE_TAG = 'tbl'
    
    para_idx = 0
    tbl_idx = 0
    
    index_dict = {}

    for idx, elem in enumerate(body_element):
        tag = elem.tag.split("}")[-1]  # Extract tag name (ignore namespace)

        if tag == PARAGRAPH_TAG:
            index_dict[idx] = (tag, para_idx)
            para_idx += 1
        elif tag == TABLE_TAG:
            index_dict[idx] = (tag, tbl_idx)
            tbl_idx += 1
        else:
            index_dict[idx] = (tag, None)

    return index_dict