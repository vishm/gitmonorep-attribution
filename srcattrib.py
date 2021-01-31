
import sys
import re
import fileinput
import json
import os

class JiraMatcher:
    def __init__(self:any, jira_prefix: str):
        self._jiraprefix = jira_prefix

    def match(self:any, changedesc: str):
        strMatch = "(" + self._jiraprefix + "-\d*)[,: ]"
        return re.findall(strMatch, changedesc)

class Change:
    def __init__(self: any, jiramatcher: JiraMatcher, changedesc: str):
        self._changedesc = changedesc
        self._files = []
        self._jiras = jiramatcher.match(changedesc)

    def add(self:any, filename: str):
        self._files.append(filename)        

    def isImpactByChange(self:any, rootFolders: list):
        for folder in rootFolders:
            for file in self._files:
                filepath = os.path.dirname(file)
                filename = os.path.basename(file)

                if len(filename) == 0:
                    continue
                
                if folder == "/" and len(filepath) == 0:
                    return True

                if filepath.startswith(folder):
                    return True

        return False

    def describe(self:any, showFiles: bool):
        print("Change: ", self._changedesc)

        if showFiles:
            for file in self._files:
                print(file)

# Application folder definition, including dependent folders.
def get_application_definition():
    script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    application_def_files = script_path + "/application_def.json"
    with open(application_def_files, "r") as file:
        data=file.read()

    applicationDefinitions = json.loads(data)
    
    return applicationDefinitions

# Use inconjuction with 
# git show --name-only  9ba7577..33a647b --oneline
# where the starting sha (which isn't inluded) to the end sha
def main(argv):    
    # application definition    
    dumpApp = argv[1]
    jiraprefix = "JIRA" ## defautl prefix to find
    if (len(argv) >= 3):
        jiraprefix = argv[2]

    print("Determining changes for", dumpApp,'matching Jira tag',jiraprefix,'...')

    jiraMatcher = JiraMatcher(jiraprefix)

    # Definition of individual app folders and dependent folders.
    appDefs = get_application_definition()
    
    # Build up internal structure of changes(change description, files and jira)
    changes = []
    latestChange = None
    line = sys.stdin    
    for line in sys.stdin:
        # Check if git sha, if so create a new Changes object to track those files.
        match = re.match('^[0-9,a-f]+\s', line)
        line = line.strip('\n')        
        if match:            
            latestChange = Change(jiraMatcher, line)
            changes.append(latestChange)
        else:            
            latestChange.add(line)        

    # build up list of changes associated with each application definition (appdef)
    appChanges = {}
    for ch in changes:
        for appName in appDefs:
            if ch.isImpactByChange(appDefs[appName]):
                if (appName not in appChanges):
                    appChanges[appName] = []
                
                appChanges[appName].append(ch)

    # output the changes only as pertains to application of interest
    jiras = []
    for appName in appChanges:
        if appName!=dumpApp:
            continue
        print(appName, "has the following", len(appChanges[appName]), "change(s)")
        for change in appChanges[appName]:
            change.describe(False)
            jiras =  jiras + (change._jiras)

        print("All Jiras: ", set(jiras))



if __name__ == "__main__":
    main(sys.argv)