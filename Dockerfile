FROM python:3-onbuild

MAINTAINER Eduard Kibort

VOLUME /repository
VOLUME /code 

WORKDIR /code

CMD ["/code/run.sh"]

