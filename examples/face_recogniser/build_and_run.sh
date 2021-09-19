#!/bin/bash
app="face_recogniser"
docker build -t ${app} .
docker stop ${app}
docker rm ${app}
docker run \
  -p 56733:80 \
  --add-host=host.docker.internal:host-gateway \
  --name=${app} \
  -v /etc/baltic/face_recogniser/configs:/app/module/configs/ \
  ${app}
