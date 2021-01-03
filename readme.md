# Mainline source attribution

The background of this simple script is for collating changes for an application & library set that maybe for a mono git repo and reporting it up correctly.

For example, we may have within a mono repo, app1 and lib1, any changes to lib1 should be reported as implicitly a change to app1. The python script below simply attributes the changes as detected by git into the relevant buckets as pertains to the application definition.

````
git show --name-only  9ba7577..0992e8d --oneline | python3 srcattrib.py app1
````

All relevant Jiras will be source from the changes in the description.


## Application Definition
The makup of the application by it's top level folders can be found in the function get_application_definition as follows, here we see app1 pertains to the sources held in folder "app1" and "lib1"

````
def get_application_definition():
    applicationDefinitions =  {
        'app1' : ['app1', 'lib1'],
        'app2' : ['app2']
    }

    return applicationDefinitions
````