# pull official base image
FROM python:3.8-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN python -m venv /env \
    && /env/bin/pip install --upgrade pip
COPY ./requirements.txt .
RUN /env/bin/pip install --no-cache-dir -r ./requirements.txt


ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]