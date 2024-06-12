# README #
API AUXIP backend.

### Backend start-up with Poetry ###
```
AUXIP_DEBUG_MODE=true poetry run uvicorn auxip_backend.main:app --host 0.0.0.0 --reload --log-level debug
```

### Tests ###

* Execute the tests

```
poetry run pytest -s test/test_main.py
poetry run pytest -s test/test_main.py -k test_put_subscription_status
```


### Code formattng ###

* Verify the code style:

```
poetry run black .
poetry run isort . --profile black
poetry run flake8 .
```

### Dependencies management ###

* management of dependencies with poetry
```
poetry add sqlalchemy
poetry add sqlalchemy_guid
poetry add psycopg2
poetry add fastapi[all]
```
* install dependencies with pip
```
pip install -r requirements.txt
```
