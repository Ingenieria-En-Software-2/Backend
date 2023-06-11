# Backend

## Setup

Add .env in the root folder and add the following variables:

```bash
POSTGRES_USER='<YOUR_POSTGRES_USER>'
POSTGRES_PASSWORD='<YOUR_POSTGRES_PASSWORD>'
POSTGRES_DB='<YOUR_POSTGRES_DATABASE>'
SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://<YOUR_POSTGRES_USER>:<YOUR_POSTGRES_PASSWORD>@<POSTGRES_HOST>:5432/<YOUR_POSTGRES_DATABASE>'
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

to create migrations folder:

```bash
flask db init
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
