 # Backend

## Setup

Add .env in the root folder and add the following variables:

```bash
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db name>
SQLALCHEMY_DATABASE_URI=<postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB} >
```

## Run Backend + DB with docker compose

```bash
docker-compose up --build <service> -d
```
The \<service> corresponds with backend and postgres services. Leave empty for
running both services.

In localhost, backend and postgres services will be started at 9010 and 5432
ports respectively

## Run Backend + DB locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

to create the tables in the database:

```bash
flask db migrate
flask db upgrade
```

to run the backend:

```bash
flask run
```



