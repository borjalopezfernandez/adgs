# README #
AUXIP Auxiliary Interface Point tests.


### Dependencies ###
* init local development database:
```
sudo service postgresql start

```

### Tests ###

* Unit tests
```
pytest -s main_test_unit.py
```

* Integration tests
```
pytest --log-cli-level=debug -s main_test_integration.py
pytest --log-cli-level=debug -s main_test_integration.py -k test_subscription_cycle
```