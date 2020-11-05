FROM python:3.7.2-slim

ENV PYTHONUNBUFFERED 1

ENV RUNTIME_PACKAGES \
    gettext \
    libfbclient2

ENV BUILD_PACKAGES \
    python2.7-dev \
    libev-dev \
    gcc \
    git

RUN apt-get update && \
    apt-get upgrade -y && \
    pip install wheel pipenv

RUN apt-get install -y --no-install-recommends $BUILD_PACKAGES && \
    apt-get install -y --no-install-recommends $RUNTIME_PACKAGES && \
    apt-get install -y --no-install-recommends curl

WORKDIR /application
COPY Pipfile /application
COPY Pipfile.lock /application
RUN set -ex && pipenv install --deploy --system --dev
RUN apt-get remove -y $BUILD_PACKAGES

RUN adduser --disabled-password --uid 1000 expedition_merman_wrapper --home /application && \
    chown -hR expedition_merman_wrapper: /application

USER expedition_merman_wrapper

COPY .flake8 /application
COPY conftest.py /application
COPY pytest.ini /application
COPY .coveragerc /application
COPY manage.py /application

ADD ./expedition_merman_wrapper /application/expedition_merman_wrapper
ADD ./tests /application/tests
ADD ./uwsgi /application/uwsgi

RUN mkdir /application/run

EXPOSE 8000

CMD ["python", "manage.py", "uwsgi"]
