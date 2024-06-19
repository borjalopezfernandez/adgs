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
