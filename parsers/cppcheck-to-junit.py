import sys
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

def parse(input_file, output_file):
    
    # Read data from input
    xml_data = input_file.read()

    root = ET.fromstring(xml_data)

    errors = root.find('./errors')

    current_datetime = datetime.now()
    datetime_string = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')

    # Collect all UNIQUE path to test error
    filepaths = []

    for error in errors:
        location = error.find('location')
        location_file = location.get('file')

        if location_file not in filepaths:
            filepaths.append(location_file)

    # Write the header
    output_file.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Cppcheck">
    <testsuite name="Cppcheck" timestamp="{datetime_string}" hostname="runner-gxoufpx2-project-27-concurrent-0" tests="{len(filepaths)}" errors="{len(errors)}" failures="0" skipped="0" time="3.0">""")

    # Write errors in groups named <testcase>
    for path in filepaths:
        output_file.write(f"""\n\t<testcase name="{path}" classname="Cppcheck error" time="1.0">""")

        for error in errors:
            # Get information about error file
            location = error.find('location')
            location_file = location.get('file')

            # Get the rest of the information to write it in .xml file
            if location_file == path:
                error_id = error.get('id')
                error_severity = error.get('severity')
                error_msg = error.get('msg')
                error_info = error.get('info')
                location_file0 = location.get('file0')
                location_line = location.get('line')
                location_column = location.get('column')

                output_file.write(f"""\n\t<error message="{error_msg}" type="{error_severity}:{error_id}">""")
                
                output_file.write(f"""{location_file0 if location_file0 else location_file} {error_msg} {location_file}:{location_line}:{location_column}: {error_info if error_info else ""}</error>""")
        output_file.write("""\n\t</testcase>""")
    
    output_file.write("""\n</testsuite>\n</testsuites>""")



if __name__ == "__main__":
    # If number of given arguments are less than 2, exit
    if len(sys.argv) < 2:
        logging.error("Usage: %s base-filename-path", sys.argv[0])
        logging.error(
            "  base-filename-path: Removed from the filenames to make nicer paths.")
        sys.exit(1)
    
    parse(sys.stdin, sys.stdout)