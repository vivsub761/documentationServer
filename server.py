from flask import Flask, request
import json
import base64
from updateDocumentation import astUpdater
from waitress import serve
app = Flask(__name__)




@app.route("/", methods = ["Post"])
def getDocumentation():
    '''
        data comes from front end in format
        {encoded_file_data: b64encodedString}
    '''
    print("REQUEST RECEIVED")
    data = request.get_json()
    decoded_data = base64.b64decode(data["encoded_file_data"])
    documentationFetcher = astUpdater(decoded_data)
    return documentationFetcher.getDocumentation()


if __name__ == "__main__":
    print("RUNNING")
    serve(app, host='0.0.0.0', port=14366)
