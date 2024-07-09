# README #
ADGS security.

### Deployment ###

* Production environment

### Build ADGS NGINX docker image ###

Build the production image (name of the image should be app_adgs_nginx):

* Build
```
docker build --build-context nginx_configuration_directory=nginx --build-arg NGINX_CONFIGURATION=nginx.conf -f nginx/Dockerfile -t app_adgs_nginx:latest .
```

### Export docker image ###

Export the production image (name of the image should be app_adgs_nginx plus the version):

* Export image
```
docker save app_adgs_nginx > /tmp/app_adgs_nginx-0.0.1.tar
```

### Build ADGS Keycloak docker image ###

Build the production image (name of the image should be app_adgs_keycloak):

* Build
```
docker build -f keycloak/Dockerfile -t app_adgs_keycloak:latest .
```

### Export docker image ###

Export the production image (name of the image should be app_adgs_keycloak plus the version):

* Export image
```
docker save app_adgs_keycloak > /tmp/app_adgs_keycloak-0.0.1.tar
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
