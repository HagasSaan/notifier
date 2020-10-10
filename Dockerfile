FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /application
WORKDIR /application
COPY requirements.txt /application/
RUN pip install -r requirements.txt
COPY ./notifier /application/notifier
WORKDIR /application/notifier
CMD python manage.py runserver 0.0.0.0:8000
