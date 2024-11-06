FROM python:3.10-slim
COPY ./db.py /db.py
COPY ./llm_service.py /llm_service.py
COPY ./queue_consumer.py /queue_consumer.py
COPY ./service.py /service.py
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "service.py"]