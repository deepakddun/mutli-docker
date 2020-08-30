FROM python:3-alpine

COPY ./requirements.txt .


RUN pip install -r requirements.txt

# RUN pip install psycopg2==2.7.5

COPY . .

CMD ["gunicorn","-b","0.0.0.0","run:app","--log-level debug"]
