#
# Copyright (C) 2017 Duckbills Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

ARG PLATYPUS_BASE_IMAGE_TAG=testing 
FROM duckbills/platypus:"${PLATYPUS_BASE_IMAGE_TAG}" 

LABEL org.label-schema.name='duckbills/platypus-oss' 
LABEL org.label-schema.description='Platypus OSS.' 
LABEL org.label-authors='Duckbills Platypus OSS.'

RUN apt-get update && \
    apt-get install -y golang-go python3 python3-venv wget unzip htop jq strace sudo \
    git vim curl lsof ssh

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN \
  mkdir -p /user/app/primary_index/ \
  && mkdir -p /user/app/primary_state/ \
  && mkdir -p /user/app/primary_archiver \
  && mkdir -p /user/app/replica_index \
  && mkdir -p /user/app/replica_state \
  && mkdir -p /user/app/replica_archiver \
  && mkdir -p /user/app/config \
  && mkdir -p /user/app/log
#
# Copy the application:
COPY deploy_app.py .
ARG BOTO_CFG=boto.cfg
COPY ${BOTO_CFG} /user/app/config/boto.cfg

EXPOSE 8900/tcp
EXPOSE 8902/tcp

#
#USER platypus
#WORKDIR /opt/platypus
#https://stackoverflow.com/questions/57857165/passing-args-to-python-script-inside-dockerfile
ARG BUCKET_NAME=platypus-test1
ENV BUCKET_NAME=$BUCKET_NAME
ARG SERVICE_NAME=platypus-single-node
ENV SERVICE_NAME=$SERVICE_NAME
ARG RESTORE_STATE=no
ENV RESTORE_STATE=$RESTORE_STATE
ENTRYPOINT ["sh", "-c", "python3 -u deploy_app.py /user/app /user/app/config/boto.cfg ${BUCKET_NAME} ${SERVICE_NAME} ${RESTORE_STATE}"]


