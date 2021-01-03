
import sys
import re
import fileinput

class Change:
    def __init__(self: any, changedesc: str):
        self._changedesc = changedesc
        self._files = []
        self._jiras = re.findall("(JIRA-\d*)[,: ]", changedesc)

    def add(self:any, filename: str):
        self._files.append(filename)        

    def isImpactByChange(self:any, rootFolders: list):
        for folder in rootFolders:
            for file in self._files:
                if file.startswith(folder):
                    return True

        return False

    def describe(self:any, showFiles: bool):
        print("Change: ", self._changedesc)

        if showFiles:
            for file in self._files:
                print(file)


# Application folder definition, including dependent folders.
def get_application_definition():
    applicationDefinitions =  {
        'app1' : ['app1', 'lib1'],
        'app2' : ['app2']
    }

    return applicationDefinitions

# Use inconjuction with 
# git show --name-only  9ba7577..33a647b --oneline
# where the starting sha (which isn't inluded) to the end sha
def main(argv):
    # application definition
    dumpApp = argv[1]    
    print("Determining changes for", dumpApp,'...')

    # Definition of individual app folders and dependent folders.
    appDefs = get_application_definition()
    
    # Build up internal structure of changes(change description, files and jira)
    changes = []
    latestChange = None
    line = sys.stdin
    for line in sys.stdin:                
        # Check if git sha, if so create a new Changes object to track those files.
        match = re.match('^[0-9,a-f]{7}\s', line)
        line = line.strip('\n')        
        if match:            
            latestChange = Change(line)
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

        print("All Jiras: ", jiras)



if __name__ == "__main__":
    main(sys.argv)