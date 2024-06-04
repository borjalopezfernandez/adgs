# README #
AUXIP Auxiliary Interface Point tests.


### Dependencies ###
* init local development database:
```
sudo service postgresql start

```

* Database configuration:
```
SQLALCHEMY_DATABASE_URL = 'postgresql://adgs:adg$#5432@127.0.0.1/adgs_db'
```

### Tests ###

* Unit tests
```
pytest -s main_test_unit.py
```

* Integration tests
```
pytest -s main_test_integration.py
pytest -s main_test_integration.py -k test_subscription_cycle
```