from flask import Flask, request
import json
import base64
from updateDocumentation import astUpdater, NestedFunctionFinder
import ast
from waitress import serve

app = Flask(__name__)

@app.route("/", methods = ["Post"])
def getDocumentation():
    '''
        data comes from front end in format
        {encoded_file_data: b64encodedString}
    '''
    data = request.get_json()
    decoded_data = base64.b64decode(data["encoded_file_data"])
    tree = ast.parse(decoded_data)
    findNested = NestedFunctionFinder(tree)
    findNested.visit(findNested.tree)

    documentationFetcher = astUpdater(tree, findNested.nested)
    return documentationFetcher.getDocumentation()


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=14366)
