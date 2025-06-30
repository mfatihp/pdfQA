# Angular app
FROM node:alpine3.22 AS build

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build -- --output-path=/app/dist --configuration production

# Nginx 
FROM nginx:mainline-alpine3.22

COPY --from=build /app/dist/ /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]