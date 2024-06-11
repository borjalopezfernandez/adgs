# README #
AUXIP Auxiliary Interface Point.

### Summary ###

* Dependencies
* Development environment

### Docker TEMPORAL COMPOSE ###

* Start-up
```
docker compose -f compose_auxip.yml  --env-file env/localhost_env up -d
```

* Shutdown
```
docker compose -f compose_auxip.yml --env-file env/localhost_env down
```



### Docker image / container AUXIP ###

* Build app_adgs_auxip
```
docker build -f Dockerfile.adgs.auxip.localhost.yaml -t app_adgs_auxip:latest .
```


### Docker image / container minARC ###

* Build app_adgs_auxip

```
docker build -f Dockerfile.adgs.minarc.localhost.yaml -t app_adgs_minarc:latest .
```
