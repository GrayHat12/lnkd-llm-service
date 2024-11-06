FROM python:3.10-slim
COPY ./common_constants /common_constants
COPY ./config /config
COPY ./controller /controller
COPY ./dao /dao
COPY ./dto /dto
COPY ./exceptions /exceptions
COPY ./middlewares /middlewares
COPY ./server /server
COPY ./services /services
COPY ./utils /utils
COPY ./validations /validations
COPY ./.conf /.conf
COPY ./requirements.txt /requirements.txt
COPY ./start.py /start.py
RUN pip install -r requirements.txt
CMD ["python", "start.py", "--host","0.0.0.0","--port","8080", "--stage", "PROD"]