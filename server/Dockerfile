FROM nginx:alpine

WORKDIR /usr/share/nginx/html

RUN apk add --no-cache wget && \
    wget -P /usr/share/nginx/html https://http.cat/200.jpg

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]