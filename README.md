# Reproducing open-projects software test execution experiment

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5425240.svg)](https://doi.org/10.5281/zenodo.5425240)

Reproduction package for the paper "Testing the past: can we still run tests in past snapshots?", presented to ICSE 2022 (still under review). This package contains:

```bash
.
├── configFiles     # Config files for each project
├── dockerfiles     # Docker files for all necessary images to perform the experiment
├── notebooks       # Jupyter Notebooks for data extraction and analysis
├── previousResults # Results from previous studies
├── projects        # Subjects of the experiment (git repositories)
├── py              # Python scripts to perform the experiment
├── results         # Contains the results generate from the experiment
├── scripts         # Bash scripts to easy-perform the experiment
├── tmp             # Folder for temporary files
└── README.md 
```

Some data needed to correctly reproduce the experiment is hosted in Zenodo (https://zenodo.org/record/5425240), due to the limitations of the GitHub file size (the size of the dataset >1TB decompressed). The dataset hosted in Zenodo contains the following files:

```bash
.
├── Apache          
    ├── projects          # Repositories of each Apache project (tar.gz)
    ├── results           # Results per project (tar.gz)
├── GitHub
    ├── projects          # Repositories of each GitHub project (tar.gz)
    ├── results           # Results per project (tar.gz)
└── ManySStub4J (Many4J)          
    ├── projects          # Repositories of each Many4J project (tar.gz)
    └── results           # Results per project (tar.gz) - NOT AVAILABLE DUE SIZE (150GB) - FINAL VERSION WILL INCLUDE
```

## Set Up

*Pre-requisites to reproduce our work*

- Git 2.17+
- Docker 19+

These dependencies will be needed to download this repository, build the Docker images and run the containers from those images.

Clone the repo:

```
  $ git clone https://github.com/BuildabilityResearcher/TestabilityStudy.git
  $ cd TestabilityStudy/
```

# Conducting the experiment

The experiment was carried out in 3 phases:
- 1. Repository mining
- 2. Execution of the tests in the past
- 3. Analysis of the results

## Step 1. Repository mining

### 1.1 Datasets selected

To carry out the experiment, we have generated 3 datasets using differents sources:

- **Apache:** 100 projects selected for Tufano et.al to test their buildability, back in 2016.
- **GitHub:** GitHub API.
- **Many4J:** 100 projects selected from ManySStuBs4J dataset

### 1.2 Project mining and selection

#### Apache

- Of the original 100 Apache projects, 79 could be recovered. 
- A replication of the Tufano et.al. experiment was carried out to test the actual buildability of the projects. 
- Finally, 12 projects (those with a buildability of 10% or more) were selected.

#### GitHub

- A search for Java projects has been carried out with at least 500 stars and 300 forks,at least five years of development, active in January 2020(at least one commit, between 1,000 and 10,000 commits.
- From the results obtained, 40 projects have been randomly selected.
- We have reproduced the Tufano et.al. experiment for this set of projects to test its buildability.
- Finally, 15 projects (those with a buildability of 15% or more) were selected.

#### Many4J

- Of the 100 original projects, 2 projects already existing in other datasets, 2 projects whose repository is no longer available and 11 projects have been discarded. 
- Of the remaining 85 projects, 84 have been selected for the analysis of the study, excluding the "hazelcast" project because its implementation was unreasonably delayed.

### 1.3 How to reproduce this step

The execution of this step is implemented in a single Jupyter Notebook per dataset.

To reproduce this step:

- Build docker image Jupyter docker image locally
```
$ docker build -f dockerfiles/jupyter.Dockerfile -t jupyter-bugs .
```
- Run a docker container from this image (PWD should be root folder of the project)
```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```
- [Open notebooks in browser](http://localhost:8888/notebooks/notebooks/ProjectsMining/)
- [Open notebooks in Gitlab/GitHub](notebooks/ProjectsMining/)

INPUT: 
- Info from Original Study projects: 
    - Apache: `previousResults/TufanoResults/analyzedProjects`
    - GitHub (Own mining)
    - ManySStub4J: `previousResults/ManySStub4J/topJavaMavenProjects.csv`

OUTPUT: 
- Folder `configFiles/<dataset>Projects/` which contains all config files for next step
- All projects downloaded from GitHub at folder: `projects/`

> **Notes:**
> - Execute this experiment (download and analyze repositories) takes a considerable amount of time. 
> - If order to be able to reproduce the experiment, the following files and folders are provided:
>   - Git repositories for all datasets (available in [Zenodo dataset](https://zenodo.org/record/5425240))
>   - Config files at `configFiles/<dataset>/`

## Step 2.Execution of the tests in the past

### 2.1 Experiment process

From the configuration files generated in the previous step (Step 1), the defined commits/snapshots will be built iteratively for each project:

1. The repository is downloaded (if it does not available locally)
2. Inside the repository, it is placed in the commit you want to check
3. The build command for Maven is executed (mvn compile) inside a Docker container.
    - The success code (0 or not 0) and the log are collected 
4. The test build command for Maven is executed (mvn test-compile) inside a Docker container.
    - The success code (0 or not 0) and the log are collected
5. The test command for Maven is executed (mvn test) inside a Docker container.
    - The success code (0 or not 0) and the log are collected. All surefire-reports folders are also saved (contains results of the test in XML format)
6. Repeat steps 2-6 for the next commit.

##### 2.2 Experiment Results

For each project, a results folder is generated in the `results/` folder which the following content:

- `build_files/` A JSON file is stored in this folder for each commit that collects the tested build settings and their result (whether it worked or not)
- `general_logs/` This folder contains a general log of the execution of the experiment. If this experiment was paused and resumed later, a new log is generated.
- `logs/` This folder stores a log for each build configuration executed on a snapshot. It includes 3 folders for each execution:
    - `logs/build`
    - `logs/build_test`
    - `logs/test`
- `test_results` This folder contains, for each commit where the tests have been executed, their results in XML format.
- `report_experiment.csv` This file contains the information of the results of the experiment. For each commit, it specifies whether it was successfully built or not, the execution time required by the build, and additional information about the snapshot, such as its creation date or the comment associated with the commit (See Table 1). 

*Table 1: Commit report example* 

| id | commit   | build   | build_exec_time | test_build | test_build_exec_time | test    | test_exec_time | date                      | comment |
|----|----------|---------|-----------------|------------|----------------------|---------|----------------|---------------------------|---------|
| 0  | a0defe57 | SUCCESS | 35              | SUCCESS    | 7                    | SUCCESS | 9              | 2014-09-23 15:11:35 +0800 | init    |

### 2.3 How to reproduce this step

To reproduce this step:

- Build docker image Jupyter docker image locally
```
$ docker build -f dockerfiles/build-analyzer.Dockerfile -t  build-analyzer:0.3.3-dev .
```
- Run a docker container from this image (PWD should be root folder of the project). You need to set _<project_name>_ (i.e. `jena`) and _<path_to_config_file>_ (i.e. `configFiles/ApacheProjects/isis-config.json`)
```
$ docker run -d --rm\
    -v $PWD/results:/home/bugs/results \
    -v $PWD/py:/home/bugs/py \
    -v $PWD/projects:/home/bugs/projects \
    -v $PWD/configFiles:/home/bugs/configFiles \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /home/bugs/ \
    --name build-experiment-<project_name> \
    --privileged=true \
    build-analyzer:0.3.3-dev python py/checkBuildHistory.py <path_to_config_file>
```

To make the execution easier, a bash script per dataset is provided to launch the experimentation of a project just from its name:

```
$ ./scripts/runApacheExperiment.sh <project_name>
$ ./scripts/runGitHubExperiment.sh <project_name>
$ ./scripts/runManySStub4JTestExperiment.sh <project_name>
```

INPUT: 
- Configuration files from `configFiles/<dataset>Projects/`

OUTPUT: 
- Folders in `results/` per project as defined in section 2.2.

## Step 3. Analysis of the results

For this step you will need to have started a Docker container from the image built in step 1.3.

```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```

### 3.1 Create resume

The amount of data generated forces us to generate a handy summary of the experiment. To do so, we will use a Jupyter Notebook that will collect the metrics set in the study.

- [Open notebooks in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/TestAnalysis/CreateResume.ipynb)
- [Open notebooks in Gitlab/GitHub](notebooks/ProjectAnalysis/TestAnalysis/CreateResume.ipynb)

INPUT: 
- Raw data generated by Step 2

OUTPUT: 
- Summaries of the results for each project, grouped by dataset: 
    - results/AllResults.csv
    - results/ApacheResults.csv
    - results/GitHubResults.csv
    - results/Many4JResults.csv

### 3.2 Experimental results

From the summaries obtained in step 3.1 we show metrics at dataset level as well as different plots of the projects.

- [Open notebooks in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/TestAnalysis/ExperimentalResults.ipynb)
- [Open notebooks in Gitlab/GitHub](notebooks/ProjectAnalysis/TestAnalysis/ExperimentalResults.ipynb)

INPUT: 
- Summaries of the results from Step 3.1

OUTPUT: 
- Graphics with project results
- Tables summarising the results

### 3.3 Analyze results

In this step, a more advanced analysis of the results is made, dividing them into quartiles according to different metrics and looking for the correlation of testability with these metrics. The results for the best projects for each of the testability flavours are also provided.

- [Open notebooks in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/TestAnalysis/AnalyzeResults.ipynb)
- [Open notebooks in Gitlab/GitHub](notebooks/ProjectAnalysis/TestAnalysis/AnalyzeResults.ipynb)

INPUT: 
- Summaries of the results from Step 3.1

OUTPUT: 
- Correlation graphics
- Tables summarising the results by different metrics (Total commits, LoC or Age)

### 3.4 Preliminary study on errors causing low testability

In this notebook, an exploratory study of the causes of test execution errors is carried out.

- [Open notebooks in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/TestAnalysis/PreliminaryStudy.ipynb)
- [Open notebooks in Gitlab/GitHub](notebooks/ProjectAnalysis/TestAnalysis/PreliminaryStudy.ipynb)

INPUT: 
- Summaries of the results from Step 3.1 (errors)

OUTPUT: 
- Table with main errors on test execution
