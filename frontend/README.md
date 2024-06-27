# README #
Fron-End for the Auxiliary Data Gathering Service.

### Summary ###

* Dependencies
* Development environment

### Build docker image ###

Build the image for development associating the UID to the development environment users’ (name of the image should be app_adgsfe_dev):

* Build
```
docker build --build-arg FLASK_APP=adgsfe --build-arg UID_HOST_USER=1000 -f Dockerfile.dev -t app_adgsfe_dev:latest .
```

### Docker compose ###

Setup the docker compose pointing to the development environment:

* Start-up
```
docker compose -f compose_dev.yml  --env-file env/localhost_env_dev up -d
```

* Shutdown
```
docker compose -f compose_dev.yml  --env-file env/localhost_env_dev down
```

### ADGS Front-End URL ###

ADGS Fron-End should be available at port 5200 for development:
http://localhost:5200

* Production environment

### Build ADGS Front-end package ###

Use the development environment to generate the ADGSFE python package:

* Generate ADGSFE package inside the development environment
```
docker exec -it adgs_adgsfe_localhost_dev /bin/bash
$ cd /adgsfe/
$ python3 setup.py sdist -d /tmp/
```

* Copy package to host
```
docker cp adgs_adgsfe_localhost_dev:/tmp/adgsfe-0.0.1.tar.gz /tmp/
```

### Build docker image ###

Build the production image (name of the image should be app_adgsfe):

* Build
```
docker build --build-context adgsfe_packages_directory=/tmp --build-arg ADGSFE_PACKAGE=adgsfe-0.0.1.tar.gz -f Dockerfile -t app_adgsfe:latest .
```

### Export docker image ###

Export the production image (name of the image should be app_adgsfe plus the version):

* Export image
```
docker save app_adgsfe > /tmp/app_adgsfe-0.0.1.tar
```

### Docker compose ###

Setup the docker compose pointing to the development environment:

* Start-up
```
docker compose -f compose.yml --env-file env/localhost up -d
```

* Shutdown
```
docker compose -f compose.yml --env-file env/localhost down
```

### ADGS Front-End URL ###

AUXIP should be serving at port 8000 for production:
http://localhost:5200/docs
