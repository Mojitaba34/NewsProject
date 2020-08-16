FROM tiangolo/uwsgi-nginx-flask:python3.8


COPY . /app

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt

RUN apt update && apt install -qy libmariadbclient-dev gcc

RUN apt-get --assume-yes install ca-certificates

ENV STATIC_URL /static/

ENV STATIC_PATH /app/app/admin/static/

RUN pip3 install -r /var/www/requirements.txt


