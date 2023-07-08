# documentationServer


IMPORTANT: For each function in the file in question:
    There must be at least one docstring in the function. The very first docstring MUST contain a brief description of the function. Subsequent ones do not matter to this script.
    The function must have argument and output annotation(s), e.g. def function(x: int, y: str) -> str
    If the function returns nothing just return a dummy variable 

If running server locally:
    Make sure to install the requirements

If hosting server on a platform:
    Go into the config.py file and change the serverLink variable to the appropriate string

To run client script:
    Run python command with the flags:
        -f: the filepath to the file of functions
        -d(optional): the filepath to where to save the json, by default the script saves it to "documentation.json"
    example: "python3 client.py -f functions.py -d destination.json
