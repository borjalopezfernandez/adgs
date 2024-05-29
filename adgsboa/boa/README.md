# README #

Business Operation Analysis (BOA) for Auxiliary Data Gathering Service (ADGS).

## Local deployment

### Prequisites

You will need to have the following installed locally to deploy locally the ADGS system:

- [Docker](https://docs.docker.com/install/)

### Quick start

* Establish the development environment:
** Create the following folders in the development environment:
```
mkdir ~/workspace
mkdir ~/workspace/orc_minarc
```
** Establish the needed repositories:
```
cd ~/workspace/
git clone https://stash.elecnor-deimos.com/scm/boa/eboa.git
cd ~/workspace/eboa/
git checkout develop
cd ~/workspace/
git clone https://stash.elecnor-deimos.com/scm/boa/vboa.git
cd ~/workspace/vboa/
git checkout develop
cd ~/workspace/
git clone https://dbrosnan@bitbucket.org/borja_lopez_fernandez/adgs.git
```
** Download ORC into the workspace folder: ~/workspace/orc_minarc

* Execute the following commands
```
export FOLDER=/media/Data_2TB; $FOLDER/workspace/adgs/adgsboa/boa/init_docker_dev_environment.sh -e $FOLDER/workspace/eboa -v $FOLDER/workspace/vboa -d $FOLDER/workspace/vboa/Dockerfile.dev -o $FOLDER/workspace/orc_minarc -u boa -t $FOLDER/workspace/adgs/adgsboa/boa -p 5100 -l adgs_dev -a adgsvboa -n
```