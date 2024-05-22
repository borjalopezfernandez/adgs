# README #
AUXIP Auxiliary Interface Point.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Dependencies ###

* Summary of set up

```
sudo service postgresql start
pip install -r requirements.txt
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

* execution command:
```
uvicorn frontend.main:app --host 0.0.0.0 --reload

```

* Swagger API front-end:
```
http://localhost:8000/docs
http://localhost:8000/redoc
```

