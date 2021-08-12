## Exchange Rate API

API exposing history of exchange rates between € and different currencies based on feed from European Central Bank.

#### Disclaimer

This code is not production ready.

#### How to run the project:

1. Initialize api with following commands:

```
cp .env.example .env
docker-compose up -d web
docker-compose exec web python manage.py migrate
docker-compose up -d
```

2. Explore [API](http://localhost:8000/api/rates/) or navigate to [Swagger](http://localhost:8000/api/schema/swagger-ui/) and enjoy.
