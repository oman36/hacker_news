FROM python:3.6

WORKDIR /var/www/hacker_news

COPY api ./api
COPY hackernews ./hackernews
COPY manage.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:80