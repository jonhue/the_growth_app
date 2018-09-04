FROM node
MAINTAINER Jonas Hübotter

ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN yarn install -g webpack

# ADD package.json $APP_HOME/

ENV NODE_ENV=production \
  PATH=$APP_HOME/node_modules/.bin:$PATH

RUN yarn install

ADD . $APP_HOME

# Write the bundle.js static asset file
RUN yarn run build

# Boot the server
CMD ["yarn", "start"]
