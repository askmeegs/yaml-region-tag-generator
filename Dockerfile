# pull official base image
FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /yaml-region-tag-generator

# install ssh, git - needed to push to github
RUN apk update
RUN apk add --no-cache openssh
RUN apk add --no-cache git

# git push ssh key
ARG SSH_PRIVATE_KEY
ARG KNOWN_HOSTS
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN echo "${KNOWN_HOSTS}" > /root/.ssh/known_hosts
RUN chmod 600 /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/known_hosts
RUN echo -e "Host *\n    StrictHostKeyChecking no\n    UserKnownHostsFile=/dev/null\n" > /root/.ssh/config

# app dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /yaml-region-tag-generator/Pipfile
COPY ./push.sh /yaml-region-tag-generator/push.sh
RUN chmod +x /yaml-region-tag-generator/push.sh
RUN pipenv install --skip-lock --system --dev

# copy project
COPY crawl.py /yaml-region-tag-generator/

CMD ["python", "/yaml-region-tag-generator/crawl.py"]