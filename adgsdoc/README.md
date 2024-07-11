# README #
Documentation repository for the Auxiliary Data Gathering Service.

### Install nextcloud ###

* Generate docker image

```
docker build -f Dockerfile -t app_adgsdoc:latest .
```

* Export image
```
docker save app_adgsdoc > /tmp/app_adgsdoc-0.0.1.tar
```

* Create nextcloud DDBB
```
docker exec -it -u postgres adgs_monitoring_db /bin/bash
psql -h localhost -U postgres
CREATE DATABASE nextcloud;
```

* Configure nextcloud

Go to http://localhost:8080/

Install nextcloud choosing the admin user desired and configuring the access to the PostgreSQL DDBB by clicking on Storage & database and using the following parameters:
Database account: postgres
Database password:
Database name: nextcloud
Database host: adgs_monitoring_db

### Nextcloud helpers ###

* Log location

/var/www/nextcloud/data/nextcloud.log

* References

https://help.nextcloud.com/t/howto-running-nextcloud-over-self-signed-https-ssl-tls-in-docker/101973