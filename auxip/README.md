# README #
AUXIP Auxiliary Interface Point.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Dependencies ###

* Summary of set up and requirements

```
sudo service postgresql start
pip install -r requirements.txt
```

* Package software develoment & management with poetry

```
poetry add --group dev pytest pytest-cov black isort flake8 bandit safety
```

* Install fastapi packages

```
poetry add fastapi uvicorn httpx
```



* Configuration adgs/adg$
* Dependencies
* Database configuration:
```
SQLALCHEMY_DATABASE_URL = 'postgresql://adgs:adg$#5432@127.0.0.1/adgs_db'
```
* How to run tests
* Deployment instructions


### Execute ###

* execution command to test without root-path to hit directly the microservice:
```
uvicorn frontend.main:app --host 0.0.0.0 --reload

```


* execution command to test with nginx proxy:
```
uvicorn frontend.main:app --host 0.0.0.0 --reload --root-path /auxip

```




* Swagger API front-end:
```
http://localhost:8000/docs
http://localhost:8000/redoc
```

