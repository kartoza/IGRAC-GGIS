FROM node:13.12.0-alpine

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

COPY ./setup/frontend/buildConfig.js ./build/

# add `/webapp/node_modules/.bin` to $PATH
ENV PATH /webapp/node_modules/.bin:$PATH


# set server to run in 0.0.0.0
RUN sed -i 's/--progress --colors --port 8081/--progress --colors --host 0.0.0.0 --port 8081/g' package.json

# install dependencies
RUN npm install --silent

# Set Env variable and pass to React app
# When we finally know how to do it, implement here
#ENV REACT_APP_BACKEND $REACT_APP_BACKEND
#RUN echo "REACT_APP_BACKEND=${REACT_APP_BACKEND}" >> .env

# start app
# Using command below, we can pass env var to REACT.
# But that would cause build status not exited with 0
#RUN REACT_APP_BACKEND=$REACT_APP_BACKEND npm start
CMD ["npm", "start"]

# Set variable to better handle terminal commands
ENV TERM xterm

EXPOSE 8081
