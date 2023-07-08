import requests
import base64
import json
import argparse
import config



def getJson(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    encoded_data = base64.b64encode(data).decode('utf-8')
    headers = {'Content-Type': 'application/json'}
    data = {"encoded_file_data": encoded_data}
    response = requests.post(config.serverLink, json=data, headers = headers)

    formatted_data = json.dumps(response.json(), indent = 4) 
    with open(args.destination, "w") as f:
        f.write(formatted_data)

parser = argparse.ArgumentParser(description="Takes in a file of functions and returns a json object that describes them in the following format {'function_name': {'Description': text, 'Inputs': {'nameOfInput': 'typeofInput',...}, 'Outputs': {'nameOfOutput': 'typeofOutput',....}}, ...}")
parser.add_argument("-f", "--targetFile", help = "Filepath to file containing functions")
parser.add_argument("-d", "--destination", default = "documentation.json", help = "Filepath to put resultant JSON. Default is documentation.json")
args = parser.parse_args()
if not args.targetFile:
    print("Please input path to file with functions when running this file with the flag -f")
    exit()

getJson(args.targetFile)



