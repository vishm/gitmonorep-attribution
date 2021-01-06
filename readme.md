# Mainline source attribution

The background of this simple script is for collating changes for an application & library set that maybe part of a mono git repo and reporting it up correctly.

For example, we may have within a mono repo, app1 and lib1, any changes to lib1 should be reported as implicitly a change to app1. The python script below simply attributes the changes as detected by git into the relevant buckets as pertains to the application definition.

````
git show --name-only  9ba7577..0992e8d --oneline | python3 srcattrib.py app1
````

All relevant Jiras will be source from the changes in the description.


## Application Definition
The script makes use of an `application_def.json` files that defines the makup of the application by it's top level folders. For example the below json, we see app1 pertains to the sources held in folder "app1" and "lib1"

````
{
    "app1" : ["app1", "lib1"],
    "app2" : ["app2"]
}
````

## Jira capture

A second argument argument to the script can be provide to indicate the Jira/change prefix to search for, in the case below, we wish to seach for change items "DEMO". If this parameter isn't specified, it'll default to JIRA

```
python3 srcattrib.py app1 DEMO
```

## Sample output of script

```
Determining changes for app1 matching Jira tag JIRA ...
app1 has the following 4 change(s)
Change:  0992e8de JIRA-10, JIRA-11: refactor
Change:  e5156969 JIRA-101: appfile1 change1
Change:  d9e5884e JIRA-1: lib1 update again
Change:  f9e5884e JIRA-1: lib1 update
All Jiras:  {'JIRA-101', 'JIRA-1', 'JIRA-11', 'JIRA-10'}

```