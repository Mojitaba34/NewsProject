FROM tiangolo/uwsgi-nginx-flask:python3.8


RUN echo "uwsgi_read_timeout 100s;" > /etc/nginx/conf.d/custom_timeout.conf
RUN echo "uwsgi_send_timeout 100s;" > /etc/nginx/conf.d/custom_timeout.conf

COPY . /app

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt

COPY /app/static/ /var/www/static/

RUN apt-get update && apt-get install -qy libmariadbclient-dev gcc

RUN apt-get --assume-yes install ca-certificates

ENV STATIC_URL /assets/

ENV STATIC_PATH /var/www/static/

RUN pip3 install -r /var/www/requirements.txt


