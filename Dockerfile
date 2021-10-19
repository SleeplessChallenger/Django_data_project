FROM python:3.9-buster

RUN pip install pipenv

WORKDIR /app
EXPOSE 8000

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY . .

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]