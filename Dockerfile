FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER True

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

RUN ["chmod", "+x", "/code/start.sh"]

EXPOSE 8000