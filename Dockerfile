FROM python:3.10-slim

ENV PIP_ROOT_USER_ACTION=ignore
ENV ENV=dev

WORKDIR /app

COPY . .

COPY ./deploy/nginx.conf /etc/nginx/conf.d/default.conf

RUN apt-get update && apt-get install nginx -y

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install --without dev

RUN chmod +x ./deploy/entrypoint.sh

CMD ["./deploy/entrypoint.sh"]