import sys
import git
import json
from loc import calculateLOC

ROOT = "/home/jovyan/work/"
sys.path.append(ROOT+"py/")

DELIMITER="|=|"

from Report import Report
from GitManager import GitManager

def addLoCToReport(config_file_path):

    config = {}

    with open(config_file_path) as config_file:
        config = json.load(config_file)

    project_path = "%s/projects/%s/" % (ROOT,config['project'])

    gm = GitManager(project_path,config['last_commit'])

    report = Report("%s/notebooks/ProjectAnalysis/TestAnalysis/results/%s/report.csv" % (ROOT, config['project']))

    for c_hash, commit in report.getRows():

        if 'files' not in commit or commit['files'] == '':

            gm.change_commit(c_hash)
            files, loc = calculateLOC(project_path,"Java","**/*.java")
            commit['files'] = files
            commit['loc'] = loc
            report.updateReport(report.HEADERS+['files','loc'])
    
    print("Finish ")


if __name__ == "__main__":
    
    # python notebooks/ProjectAnalysis/LoCAnalysis/LoCAnalysis.py configFiles/ManySStub4JProjects/spring-cloud-microservice-example-config.json
    addLoCToReport(sys.argv[1])