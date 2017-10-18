FROM python:3-onbuild

MAINTAINER Eduard Kibort

VOLUME /repository
VOLUME /report.html

COPY *.py run.sh /code/

WORKDIR /code

CMD ["/code/run.sh"]

