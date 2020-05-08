# encampments
Encampment tracker, originally for the City of Oakland

## Basic setup

```
docker-compose build
docker-compose run web python manage.py migrate
docker-compose up web
```