FROM tiangolo/uwsgi-nginx-flask:python3.8


COPY . /app

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt

RUN apt update && apt install -qy libmariadbclient-dev gcc

RUN apt-get --assume-yes install ca-certificates


RUN pip3 install -r /var/www/requirements.txt


