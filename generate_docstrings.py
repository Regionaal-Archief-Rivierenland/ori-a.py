import dataclasses
import xml.etree.ElementTree as ET
import ORI_A
import textwrap

ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
root = ET.parse("ORI-A.xsd").getroot()

for complex_type in root.findall(".//xs:complexType", namespaces=ns):
    type_name = complex_type.get("name")

    # FIXME: the complexType under ORI-A currently has no associated name
    if not type_name:
        print("skipping")
        continue

    # classes are UpperCamelCase
    class_name = type_name[0].upper() + type_name[1:]

    # get class from module
    cls = getattr(ORI_A, class_name)
    python_ordered_fields = dataclasses.fields(cls)

    for field in python_ordered_fields:
        elem = complex_type.find(f"./xs:sequence/xs:element[@name='{field.name}']", namespaces=ns)
        elem_docstring = elem.find("./xs:annotation/xs:documentation", namespaces=ns).text
        elem_docstring = "\n".join(
            textwrap.wrap(elem_docstring, width=82, subsequent_indent="  ")
        )
        print(field.name, elem_docstring)


    class_docstring = complex_type.find("./xs:annotation/xs:documentation", namespaces=ns)
