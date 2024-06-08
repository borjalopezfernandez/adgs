# README #
AUXIP Auxiliary Interface Point.

### Summary ###

* Dependencies
* Development environment


### Dependencies ###

* Postgres start in the development environment:
```
sudo service postgresql start
```


### Development environment ###

## Management of the python with virtual environments ##

* Creation
```
python -m venv venv
python -m venv venv --system-site-packages

```

* Activation
```
source venv/bin/activate
```

* Deactivation
```
deactivate
```

## Package management ##

* Install dependencies

```
pip install -r requirements.txt
```

* Inspect installed package baseline
```
python -m pip list
python -m pip freeze
```


## Poetry management ##

* Package software develoment & management with poetry

```
poetry add --group dev pytest pytest-cov black isort flake8 bandit safety
```

* Install fastapi packages

```
poetry add fastapi uvicorn httpx
```

