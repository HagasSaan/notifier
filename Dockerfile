FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /application
WORKDIR /application
COPY requirements.txt /application/
RUN pip install -r requirements.txt
COPY . /application/
WORKDIR /application/notifier
ENTRYPOINT python manage.py runserver 0.0.0.0:8000
