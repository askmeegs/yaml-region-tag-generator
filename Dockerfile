# pull official base image
FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /yaml-region-tag-generator

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /yaml-region-tag-generator/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY crawl.py /yaml-region-tag-generator/

CMD ["python", "/yaml-region-tag-generator/crawl.py"]