'''

'''

import xml.etree.ElementTree as ET
import pandas as pd
import tempfile
import shutil

def create_tempfile_of_xml_without_header(fn):
    '''
    export.xml has a header that is not valid XML. This function creates a temporary file that is a copy of export.xml, but without the header.
    '''
    with open(fn, 'r') as xml_file:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    
        # Copy the XML content to the temporary file, excluding the DTD section
        passed_header = False
        for _,line in enumerate(xml_file):
            if '<HealthData locale=' in line:
                passed_header = True
            if passed_header:
                temp_file.write(line)
    temp_file.close()
    return temp_file

def parse_export(fn: str) -> pd.DataFrame:
    '''
    parse the export.xml and return a dataframe with the data. 
    '''
    assert('export_cda' not in fn)
    # create tempoary xml_file without the heading 
    temp_file = create_tempfile_of_xml_without_header(fn)

    # Pass tree returning data with value. 
    tree = ET.parse(temp_file.name)
    root = tree.getroot()
    data = []
    for record in root.findall(".//{*}Record"):
        if not "value" in record.attrib:
            continue
        data.append(
            [
                record.attrib["type"],
                record.attrib["creationDate"],
                record.attrib["startDate"],
                record.attrib["endDate"],
                record.attrib["value"],
            ]
        )

    return pd.DataFrame(
        data=data, columns=["type", "creationDate", "startDate", "endDate", "value"]
    )


if __name__ == "__main__":
    df = parse_export("temp/apple_health_export/export.xml")
    print(len(df))
