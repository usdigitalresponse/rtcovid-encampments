# encampments
Encampment tracker, originally for the City of Oakland

## Basic setup

```
docker-compose build
docker-compose run web python manage.py migrate
docker-compose up web
```

## Adding dependencies
1. Add the dependency to `common.base`, `dev.in` or `prod.in`
2. Run `pip-compile --no-annotate reqs/dev.in`
2. Run `pip-compile --no-annotate reqs/prod.in`

## Setup Precommit Hooks
1. `pip install pre-commit`
2. `pre-commit install`

## Bootstrapping some encampment data
1. `docker-compose run web python manage.py bootstrap_location oakland` (or other supported location)
