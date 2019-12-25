FROM python:alpine3.7 
ENV PYTHONBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY Pipfile Pipfile

ARG username
RUN adduser -D ${username}  
RUN chown -R ${username} /app

RUN apk add --no-cache --virtual .build-deps gcc \
    build-base mysql-client mariadb-dev freetds-dev libffi-dev \
    && apk add --no-cache mariadb-client-libs make \
    && pip3 install pipenv 

USER ${username}  
RUN pipenv install 
USER root

RUN su -l ${root} \
    && find /usr/local \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' + \
    && runDeps="$( \
    scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | sort -u \
    | xargs -r apk info --installed \
    | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps 

USER ${username}  

COPY . /app