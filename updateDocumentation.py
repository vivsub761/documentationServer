import json
import ast
import argparse
import base64 as b64

# Class: astUpdater:
    # Fields: 
        # self.tree -> An ast tree that represents the data in the file bing read
    # Methods:
        # Initializer(decodedData) -> takes in decoded data and parses it into ast Tree, sets object variables
        # updateFileData(newData) -> given new data, changes self.tree to the contents of the new data
        # getDocumentation() -> Gets the documentation for the data in self.tree

class astUpdater:
    def __init__(self, decodedData):
        self.tree = ast.parse(decodedData)
    
    def updateFileData(self, newData):
        self.tree = ast.parse(newData)

    def __getExpectedOutputs(self, astNode):
        def returnOutputName(element):
            # This checks if the return value is a constant or a variable and returns the appropriate value
            if isinstance(element, ast.Name):
                return element.id
            elif isinstance(element, ast.Constant):
                return element.value
            return ""

        outputs = {}
        outputNames = []
        # if the last line is a tuple, then there are multiple return values
        if isinstance(astNode.body[-1].value, ast.Tuple):
            # iterate through each return value and add the variable name
            for element in astNode.body[-1].value.elts:
                outputNames.append(returnOutputName(element))
        else:
            # otherwise there is only one return value, just add it
            outputNames.append(returnOutputName(astNode.body[-1].value))
        outputTypes = []

        # gets returns types as string
        ret = ast.unparse(astNode.returns).strip()
        # if ret starts with tuple, there are multiple 
        if ret.startswith("Tuple"):
            # remove the 'Tuple[' from the beginning and the ']' from the end
            res = ret[6:-1].split(",")
            # split and remove spaces to get individual types
            outputTypes = [s.strip() for s in res]
        else:
            outputTypes = [ret]

        # add output names and types to json and return it
        for outName, outType in zip(outputNames, outputTypes):
            outputs[outName] = outType
        return outputs
    
    def __getExpectedArgs(self, astNode):
        args = {}
        for arg in astNode.args.args:
            if not arg.annotation:
                print("No annotation for expected input type. Please add it and try again")
                return {}
            args[arg.arg] = ast.unparse(arg.annotation).strip()
        return args


    def getDocumentation(self):
        # stores results
        functionDict = {}
        # create abstract snytax tree from read data
        for node in ast.walk(self.tree):
            # check if the node corresponds to a function
            if isinstance(node, ast.FunctionDef):
                # populate json
                functionDict[node.name] = {}
                docstring = ast.get_docstring(node).strip().replace("\n", " ").split()
                functionDict[node.name]["Description"] = " ".join(docstring)
                functionDict[node.name]["Input(s)"] = self.__getExpectedArgs(node)
                functionDict[node.name]["Output(s)"] = self.__getExpectedOutputs(node)  
        return functionDict
    




        



# parser = argparse.ArgumentParser(description="Takes in a file of functions and returns a json object that describes them in the following format {'function_name': {'Description': text, 'Inputs': {'nameOfInput': 'typeofInput',...}, 'Outputs': {'nameOfOutput': 'typeofOutput',....}}, ...}")
# parser.add_argument("-f", "--targetFile", help = "Filepath to file containing functions")
# args = parser.parse_args()
# if not args.targetFile:
#     print("Please input path to file with functions when running this file with the flag -f")
#     exit()
# libraryReader = astUpdater(args.targetFile)
# res = libraryReader.getDocumentation()
# with open("documentation.json", "w") as f:
#     json.dump(res, f)




