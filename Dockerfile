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

# app dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /yaml-region-tag-generator/Pipfile
COPY ./clone_prep.sh /yaml-region-tag-generator/clone_prep.sh
COPY ./push.sh /yaml-region-tag-generator/push.sh
RUN chmod +x /yaml-region-tag-generator/push.sh
RUN chmod +x /yaml-region-tag-generator/clone_prep.sh
RUN pipenv install --skip-lock --system --dev

# copy project
COPY crawl.py /yaml-region-tag-generator/

CMD ["python", "/yaml-region-tag-generator/crawl.py"]