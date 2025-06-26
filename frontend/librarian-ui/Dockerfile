# Angular app
FROM node:alpine3.22 AS build


COPY package.json package-lock.json ./

RUN npm install

COPY . .
ARG APP_NAME=librarian-ui

# Nginx 
FROM nginx:alpine


RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]