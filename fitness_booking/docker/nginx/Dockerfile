# official nginx image
FROM nginx:1.25-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir -p /var/www/certbot

EXPOSE 80
EXPOSE 443