# The Growth App

Encourage, track & analyze personal growth. Inspired by [@johnafish](https://github.com/johnafish)'s Growth Book.

**https://thegrowthapp.com**

### Development

The Growth App has a frontend built with [Redux](https://redux.js.org/) bundled
using [Webpack](https://webpack.js.org/) with dependencies handled by
[Yarn](https://github.com/yarnpkg/yarn). The backend uses
[Django](https://www.djangoproject.com/).

[Docker](https://www.docker.com/) is being used to build this project.

1. Clone this repository

    `$ git clone ssh://git@github.com/jonhue/the_growth_app.git`

2. Credentials setup

    Duplicate [.env.sample](.env.sample) to `.env`

4. Database setup

    `$ python3 backend/manage.py migrate`

5. Start development server

    ```
    $ docker-compose up
    ```

### Testing

```
# backend

# frontend
$ yarn run test
```

### Deployment

The `master` branch of this repository is automatically deployed on Heroku.

### Error tracking

### Performance tracking
