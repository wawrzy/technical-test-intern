#!/usr/bin/python3

import argparse
import ast
import json


def getParams():
    """
    Parse arguments

    :return: returns params
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    parser.add_argument("changes_list_file")
    return parser.parse_args()

def getFileContent(path):
    """
    Get file content

    :param path: Path of the file
    :return: returns file content
    """
    with open(path, 'r') as content_file:
        content = content_file.read()
    return content

def writeFile(path, content):
    """
    Write text in file

    :param path: Path of the file
    :param content: Content of the file
    :return: returns nothing
    """
    with open(path, 'wb') as target:
        target.write(bytearray(content, "utf8"))

def applyChanges(jsonConfig, changesRaw):
    """
    Apply changes in the config file

    :param jsonConfig: Json config
    :param changesRaw: Changes to apply
    :return: returns new config file content
    """
    changesList = changesRaw.split("\n")
    for changeRow in changesList:
        configVariablePath, newValue = changeRow.split(":")
        newValue = newValue.strip()
        currentData = jsonConfig
        pathList = ast.literal_eval(configVariablePath).split(".")
        for elem in pathList[:-1]:
            currentData = currentData.get(elem,{})
        currentData[pathList[-1]] = ast.literal_eval(newValue)
    return jsonConfig

def main():
    params = getParams()

    contentConfigFile = getFileContent(params.config_file)
    contentChangesFile = getFileContent(params.changes_list_file)
    jsonConfig = json.loads(contentConfigFile)

    newConfig = applyChanges(jsonConfig, contentChangesFile)

    writeFile("result.json", json.dumps(newConfig, indent=4))

if __name__ == "__main__":
    main()