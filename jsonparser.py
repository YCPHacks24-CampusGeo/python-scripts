# ssh ubuntu@map.ycp.campusgeo.com -i .\Downloads\VM_CampusGeo_Map.key
# ssh ubuntu@api.ycp.campusgeo.com -i .\Downloads\VM_CampusGeo_Api.key
# scp -i "C:\Users\16673\Downloads\VM_CampusGeo_Api.key" -r ubuntu@api.ycp.campusgeo.com:uploaded_locations C:\Users\16673\Downloads\


import os
import json
import base64


def parse_json_files(input_folder, output_folder):
    data_list = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                lat = data['Location']['Latitude']
                lon = data['Location']['Longitude']
                base64_jpg = data['base64JPG'].split(',', 1)[1]

                # Create tuple (filename without .json, latitude, longitude)
                data_list.append((os.path.splitext(filename)[0], lat, lon))

                # Decode base64 JPG and save as .jpg
                jpg_data = base64.b64decode(base64_jpg)
                jpg_filename = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpg')
                with open(jpg_filename, 'wb') as img_file:
                    img_file.write(jpg_data)

    return data_list


# Example usage
input_folder = "C:/Users/16673/Downloads/uploaded_locations"
output_folder = "C:/Users/16673/Downloads/python_output"
result = parse_json_files(input_folder, output_folder)

output = """
List<object> t = ["""

for location in result:
    image = location[0]
    latitude = location[1]
    longitude = location[2]

    output += f"""
    new {{
        Location = new GeoLocation({latitude}, {longitude}),
        Image = "{image}"
    }},"""

output += "\n];"
print(output)