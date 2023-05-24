FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app .
ARG SQLALCHEMY_DATABASE_URI
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
EXPOSE 9010
CMD [ "flask", "run","--host","0.0.0.0","--port","9010"]