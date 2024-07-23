def mathml_to_latex(element):
    """ Convert MathML XML element to LaTeX string. """
    # Namespace for MathML
    namespaces = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
    
    def visit_element(el):
        tag = el.tag.split('}')[-1]  # Remove namespace prefix
        
        if tag == 'r':
            return ''.join(visit_element(child) for child in el)
        
        elif tag == 't':
            return el.text or ''
        
        elif tag == 'sSup':
            base = visit_element(el.find('m:e', namespaces))
            exp = visit_element(el.find('m:sup', namespaces))
            return f"{base}^{{{exp}}}"
        
        elif tag == 'fSub':
            base = visit_element(el.find('m:e', namespaces))
            sub = visit_element(el.find('m:sub', namespaces))
            return f"{base}_{{{sub}}}"
        
        elif tag == 'sSubSup':
            base = visit_element(el.find('m:e', namespaces))
            sub = visit_element(el.find('m:sub', namespaces))
            exp = visit_element(el.find('m:sup', namespaces))
            return f"{base}_{{{sub}}}^{{{exp}}}"
        
        elif tag == 'mfrac':
            num = visit_element(el.find('m:num', namespaces))
            denom = visit_element(el.find('m:den', namespaces))
            return f"\\frac{{{num}}}{{{denom}}}"
        
        elif tag == 'mroot':
            base = visit_element(el.find('m:e', namespaces))
            index = visit_element(el.find('m:degree', namespaces))
            return f"\\sqrt[{index}]{{{base}}}"
        
        elif tag == 'm:apply':
            operator = visit_element(el.find('m:op', namespaces))
            args = [visit_element(child) for child in el.findall('m:e', namespaces)]
            if operator == 'plus':
                return '+'.join(args)
            elif operator == 'minus':
                return '-'.join(args)
            elif operator == 'times':
                return '*'.join(args)
            elif operator == 'divide':
                return '/'.join(args)
            else:
                return f"\\text{{Unknown operator: {operator}}}"
        
        # Handle other cases
        return ''.join(visit_element(child) for child in el)
    
    return visit_element(element)


def contains_mathml(element):
    xml_str = element.xml
    return '<m:' in xml_str
