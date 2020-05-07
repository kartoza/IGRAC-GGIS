FROM node:13.12.0-alpine as frontend

# Install utilities
RUN  apk update \
     && apk add nano \
     && apk add curl \
     && apk add git \
     && rm -rf /var/cache/apk/*

RUN git clone https://github.com/geosolutions-it/MapStore2

# set working directory
RUN mv MapStore2 webapp
WORKDIR /webapp

# add `/webapp/node_modules/.bin` to $PATH
ENV PATH /webapp/node_modules/.bin:$PATH

# add app
# COPY . ./

# set server to run in 0.0.0.0
RUN sed -i 's/--progress --colors --port 8081/--progress --colors --host 0.0.0.0 --port 8081/g' package.json

# install dependencies
RUN npm install --silent

# start app
CMD ["npm", "start"]

# Set variable to better handle terminal commands
ENV TERM xterm

EXPOSE 8081