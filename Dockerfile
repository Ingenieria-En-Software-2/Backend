FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app .
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
RUN sleep 5;
EXPOSE 9010
CMD [ "flask", "run","--host","0.0.0.0","--port","9010"]