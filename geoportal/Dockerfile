ARG GEOMAPFISH_VERSION
ARG GEOMAPFISH_MAIN_MINOR_VERSION

FROM camptocamp/geomapfish-tools:${GEOMAPFISH_VERSION} as builder
LABEL maintainer Camptocamp "info@camptocamp.com"

COPY requirements.txt /tmp/requirements.txt
RUN \
  python3 -m pip install --disable-pip-version-check --no-cache-dir --requirement=/tmp/requirements.txt && \
  rm --recursive --force /tmp/* /var/tmp/* /root/.cache/*

WORKDIR /app
COPY webpack.*.js Makefile CONST_Makefile /app/
COPY geoserver_gmf_geoportal/static-ngeo /app/geoserver_gmf_geoportal/static-ngeo
RUN make apps

COPY . /app

RUN make checks
RUN make build
RUN mv webpack.apps.js webpack.apps.js.tmpl

ENTRYPOINT [ "/usr/bin/eval-templates" ]
CMD [ "webpack-dev-server", "--mode=development", "--debug", "--watch", "--no-inline" ]

###############################################################################

FROM camptocamp/geomapfish:${GEOMAPFISH_MAIN_MINOR_VERSION} as runner

COPY requirements.txt /tmp/requirements.txt
RUN \
  python3 -m pip install --disable-pip-version-check --no-cache-dir --requirement=/tmp/requirements.txt && \
  rm --recursive --force /tmp/* /var/tmp/* /root/.cache/*

WORKDIR /app
COPY . /app
# Workaround, see:https://github.com/moby/moby/issues/37965
RUN true
COPY --from=builder /usr/lib/node_modules/ngeo/dist/* /etc/static-ngeo/
COPY --from=builder /etc/static-ngeo/* /etc/static-ngeo/
COPY --from=builder /app/alembic.ini /app/alembic.yaml ./
RUN chmod go+w /etc/static-ngeo/

RUN python3 -m pip install --disable-pip-version-check --no-cache-dir --editable=/app/ && \
    python3 -m compileall -q /usr/local/lib/python3.* \
        -x '/(debugpy|pipenv|.*pydev.*|networkx)/' && \
    python3 -m compileall -q /app/geoserver_gmf_geoportal -x /app/geoserver_gmf_geoportal/static.*

ARG GIT_HASH
RUN c2cwsgiutils-genversion ${GIT_HASH}

ARG PGSCHEMA
ENV PGSCHEMA=${PGSCHEMA}

ENTRYPOINT [ "/usr/bin/eval-templates" ]
CMD ["gunicorn", "--paste=/app/production.ini"]

ENV VISIBLE_ENTRY_POINT=/ \
    AUTHTKT_TIMEOUT=86400 \
    AUTHTKT_REISSUE_TIME=9000 \
    AUTHTKT_MAXAGE=86400 \
    AUTHTKT_COOKIENAME=auth_tkt \
    AUTHTKT_HTTP_ONLY=True \
    AUTHTKT_SECURE=True \
    AUTHTKT_SAMESITE=Lax \
    BASICAUTH=False \
    LOG_LEVEL=INFO \
    C2CGEOPORTAL_LOG_LEVEL=INFO \
    C2CWSGIUTILS_LOG_LEVEL=INFO \
    GUNICORN_LOG_LEVEL=INFO \
    SQL_LOG_LEVEL=WARNING \
    DOGPILECACHE_LOG_LEVEL=INFO \
    OTHER_LOG_LEVEL=WARNING \
    DEVELOPMENT=0 \
    LOG_TYPE=console
