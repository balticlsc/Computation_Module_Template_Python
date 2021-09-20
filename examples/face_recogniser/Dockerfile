FROM python:3.10.0rc2-alpine3.14
# Update & Install dependencies
RUN apk update
RUN apk add --no-cache --update \
    openssl \
    ca-certificates \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    build-base \
    linux-headers
RUN apk add cmake
RUN python -m pip install --upgrade pip
RUN apk --update add gcc libgcc musl-dev jpeg-dev zlib-dev
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/community' >> /etc/apk/repositories
RUN apk update
RUN apk add mongodb
COPY ./requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
# Install the balticlsc package (it is not in the requirements file to make the testing process faster)
RUN python -m pip install balticlsc-test==0.0.19
# Copy the module content and run the API
WORKDIR app
COPY __init__.py module/__init__.py
COPY module module/content
ENV FLASK_APP='/app/module/content/my_token_listener.py'
RUN echo $FLASK_APP
EXPOSE 80
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=80"]
