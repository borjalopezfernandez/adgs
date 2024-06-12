# README #
AUXIP Auxiliary Interface Point.

### Summary ###

* Dependencies
* Development environment

### Build docker image ###

Build the development image associating the UID and GID to the development environment users’ (name of the image should be app_adgs_auxip_dev):

* Build
```
docker build --build-arg UID_HOST_USER=1000 --build-arg GID_HOST_USER=1000 -f Dockerfile.adgs.auxip.localhost.dev.yaml -t app_adgs_auxip_dev:latest .
```

### Docker compose ###

Setup the docker compose pointing to the development environment:

* Start-up
```
docker compose -f compose_auxip_dev.yml --env-file env/localhost_env_dev up -d
```

* Shutdown
```
docker compose -f compose_auxip_dev.yml --env-file env/localhost_env_dev down
```

### AUXIP URL ###

AUXIP should be serving at port 8001 for development:
http://localhost:8001/docs

* Production environment

### Build AUXIP package ###

Use the development environment to generate the AUXIP python package:

* Generate AUXIP package inside the development environment
```
docker exec -it adgs_auxip_localhost_dev /bin/bash
$ cd /auxip/
$ python3 setup.py sdist -d /tmp/
```

* Copy package to host
```
docker cp adgs_auxip_localhost_dev:/tmp/auxip-0.0.1.tar.gz /tmp/
```

### Build docker image ###

Build the production image (name of the image should be app_adgs_auxip):

* Build
```
docker build --build-context auxip_packages_directory=/tmp --build-arg AUXIP_PACKAGE=auxip-0.0.1.tar.gz -f Dockerfile.adgs.auxip.localhost.yaml -t app_adgs_auxip:latest .
```

### Docker compose ###

Setup the docker compose pointing to the development environment:

<<<<<<< HEAD
* Start-up
```
docker compose -f compose_auxip.yml --env-file env/localhost_env up -d
```
=======
* Build gem in the repository
```
rake -f build_minarc.rake minarc:build[adgs,localhost,adgs_test_pg]
```

* Build app_adgs_auxip
>>>>>>> 6623a9569214f537de33496dea5ed29ca8c8f2ac

* Shutdown
```
docker compose -f compose_auxip.yml --env-file env/localhost_env down
```

<<<<<<< HEAD
### AUXIP URL ###

AUXIP should be serving at port 8000 for production:
http://localhost:8000/docs
=======
```
curl -k -v -u test:test --max-time 12000 --connect-timeout 60 --keepalive-time 12000 -L -f -s -X GET https://adgs_minarc:4567/dec/arc/requestArchive/*
```
>>>>>>> 6623a9569214f537de33496dea5ed29ca8c8f2ac
