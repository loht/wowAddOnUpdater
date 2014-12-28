import http.client
import json
from math import ceil
from pprint import pprint
import shutil
import urllib.request
import zipfile

ELVUI_HOST = 'www.tukui.org'

def checkForLatestVersion(currentVersion):
    latestVersion = 1.00
    for i in range(1,6,1):
        currentVersion = ceil(100 * float(currentVersion) + 1) / 100
        statusCode = getStatusCode(ELVUI_HOST, constructPath(currentVersion))
        if statusCode == 200:
            latestVersion = currentVersion
        elif statusCode == 404:
            break

    pprint('Latest Version Detected: ' + str(latestVersion))
    return latestVersion


def constructPath(version):
    version = str(version)
    basePath = '/downloads/elvui-'
    return basePath + version + '.zip'

def downloadElvUI(latestVersion, downloadPath):
    pprint('Attempting to download.')
    with urllib.request.urlopen('http://' + ELVUI_HOST + constructPath(latestVersion)) as response, open(str(latestVersion) + '.zip', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    pprint('Download Completed saved as \'' + str(latestVersion) + '.zip\'')

def getStatusCode(host, path):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", path)
    statusResponse = conn.getresponse()
    return statusResponse.status

def loadConfig():
    rawConfig = open('config.json')
    config = json.load(rawConfig)
    rawConfig.close()
    pprint('Config Loaded')
    return config

def unzipFile(filePath, extractionDirectory):
    pprint('Attempting to unzip')
    zipRef = zipfile.ZipFile(filePath, 'r')
    zipRef.extractall(extractionDirectory)
    zipRef.close()
    pprint('Unzipped Succesfully')

config = loadConfig();
latestVersion = checkForLatestVersion(config['currentVersion'])
downloadElvUI(latestVersion, '')
unzipFile('7.72.zip', config['wowPath'])
