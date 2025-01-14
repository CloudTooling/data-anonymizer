FROM python:3.9

ARG BUILD_DATE
ARG APP_VERSION

LABEL org.opencontainers.image.authors='Martin Reinhardt (martin@m13t.de)' \
    org.opencontainers.image.created=$BUILD_DATE \
    org.opencontainers.image.version=$APP_VERSION \
    org.opencontainers.image.url='https://hub.docker.com/r/cloudtooling/data-anonymizer' \
    org.opencontainers.image.documentation='https://github.com/CloudTooling/data-anonymizer' \
    org.opencontainers.image.source='https://github.com/CloudTooling/data-anonymizer.git' \
    org.opencontainers.image.licenses='Apache-2.0'

RUN apt-get -f install libxml2-dev libxslt-dev zlib1g-dev gcc

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "multi_anonymizer.py"]
