FROM node:9
MAINTAINER Jonas Hübotter

ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ADD package.json $APP_HOME/

ENV NODE_ENV=production \
  PATH=$APP_HOME/node_modules/.bin:$PATH

RUN yarn install

ADD . $APP_HOME

RUN yarn run build

CMD ["yarn", "start"]
