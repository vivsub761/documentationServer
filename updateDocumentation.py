import json
import ast
import argparse
import base64 as b64

# Class: astUpdater:
    # Fields: 
        # self.tree -> An ast tree that represents the data in the file being read
    # Methods:
        # Initializer(tree) -> takes in an ast Tree and sets object variables
        # updateFileData(newTree) -> changes self.tree to new tree
        # getDocumentation() -> Gets the documentation for the data in self.tree

# class NestedFunctionFinder(inherits from ast.NodeVisitor)
    # Fields: 
        # level -> current level of tree
        # nested -> set of strings that indicate which functions are nested and should be ignored
        # tree -> ast object
    # Methods:
        # visit_FunctionDef -> overrides ast.NodeVisitor's visit class specifically for when a node that is a function def is found.

class NestedFunctionFinder(ast.NodeVisitor):
    def __init__(self, tree):
        self.level = 0
        self.nested = set()
        self.tree = tree
        
    def visit_FunctionDef(self, node):
        if self.level > 0:
            self.nested.add(node)
        self.level += 1
        self.generic_visit(node)
        self.level -= 1


class astUpdater:
    def __init__(self, tree, nested):
        self.tree = tree
        self.nested = nested
    
    def updateFileData(self, newTree):
        self.tree = newTree

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
            if isinstance(node, ast.FunctionDef) and node not in self.nested:
                # populate json
                functionDict[node.name] = {}
                docstring = ast.get_docstring(node).strip().replace("\n", " ").split()
                functionDict[node.name]["Description"] = " ".join(docstring)
                functionDict[node.name]["Input(s)"] = self.__getExpectedArgs(node)
                functionDict[node.name]["Output(s)"] = self.__getExpectedOutputs(node)  
        return functionDict
    



