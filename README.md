# Backend

## Setup

Add .env in the root folder and add the following variables:

```bash
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db name>
```

## Run Backend + DB with docker compose

```bash
docker-compose up --build <service> -d
```
The \<service> corresponds with backend and postgres services. Leave empty for
running both services.

In localhost, backend and postgres services will be started at 9010 and 5432
ports respectively