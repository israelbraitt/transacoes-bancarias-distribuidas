FROM python:3.10

RUN pip install requests
RUN pip install django

WORKDIR /app

COPY . /app

CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8008"]
