FROM python:3.7-slim

RUN mkdir /data
COPY data/ingredients.csv data/

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY backend .
RUN mkdir /static
COPY frontend/build/static static/

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]