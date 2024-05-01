# build stage
FROM node:18-alpine as build-stage

WORKDIR /app

COPY quasar-project /app/

RUN ls -la

RUN npm install -g @quasar/cli && \
    npm i

RUN quasar build


# production stage
FROM nginx:1.26.0-alpine as production-stage
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
