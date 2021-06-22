FROM python:3.9.2
WORKDIR /code
COPY . .
RUN pip install -r ./requirements.txt
WORKDIR /code/foodgram
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
