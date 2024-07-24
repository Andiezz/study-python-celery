FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

#COPY app.py /app.py
ADD . /flask_app
WORKDIR /flask_app

CMD celery -A tasks.celery_app beat --loglevel=info
ENTRYPOINT celery -A tasks worker --loglevel=info

#-Q celery_worker
#ENTRYPOINT ['celery','-A','test_celery', 'worker', '--loglevel=info']