# README #

Auxiliary Data Gathering Service (ADGS).

## Local deployment

### Prequisites

You will need to have the following installed locally to deploy locally the ADGS system:

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- p7zip-full

If you're running Docker for Desktop for macOS or Windows, Docker Compose is already included in your installation.

### Quick start

* Download DEC, minArc and BOA images from the following folder:
https://drive.google.com/drive/folders/1gKWJW90cuKxg3cKXoa8RJc-SK17J5Fzd?usp=drive_link
* Uncompress images using '7za' and 'tar'
* Load images using 'docker load'
* Execute the following commands
\# useradd -m -o -r -u 10000 -g 10000 boa
\# useradd -m -o -r -u 2020 -g 2020 adgs
\# export PATH_TO_FOLDERS=/data/adgs/adgs_monitoring
\# mkdir -p $PATH_TO_FOLDERS
\# mkdir $PATH_TO_FOLDERS/boa_ddbb
\# mkdir $PATH_TO_FOLDERS/log
\# mkdir $PATH_TO_FOLDERS/minarc_archive
\# mkdir $PATH_TO_FOLDERS/orc_ddbb
\# mkdir $PATH_TO_FOLDERS/rboa_archive
\# mkdir $PATH_TO_FOLDERS/intray_boa
\# mkdir $PATH_TO_FOLDERS/boa_certificates_and_secret_key
\# mkdir $PATH_TO_FOLDERS/prometheus_ddbb
\# cd $PATH_TO_FOLDERS
\# chown boa:boa boa_certificates_and_secret_key log/ intray_boa/ minarc_archive/ rboa_archive/
\# chown adgs:adgs prometheus_ddbb/
\# docker compose -f compose.yml --env-file env/localhost_env up -d
\# docker exec -it -u root app_boa_localhost /bin/bash
    \# source scl_source enable rh-ruby27; boa_init.py -e -o -s -u -y
