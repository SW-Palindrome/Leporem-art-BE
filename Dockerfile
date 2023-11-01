FROM python:3.10-slim

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY . .

COPY ./deploy/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./.ssl/fullchain.pem /etc/letsencrypt/live/leporem.art/fullchain.pem
COPY ./.ssl/privkey.pem /etc/letsencrypt/live/leporem.art/privkey.pem

RUN apt-get update && apt-get install nginx -y

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install --without dev

RUN chmod +x ./deploy/entrypoint.sh

CMD ["./deploy/entrypoint.sh"]
