# The Growth App

Encourage, track & analyze personal growth. Inspired by [@johnafish](https://github.com/johnafish)'s Growth Book.

**https://thegrowthapp.com**

### Development

The Growth App uses [asdf](https://github.com/asdf-vm/asdf) as version manager.
It has a frontend built with [Redux](https://redux.js.org/) bundled using
[Webpack](https://webpack.js.org/) with dependencies handled by
[Yarn](https://github.com/yarnpkg/yarn). The backend uses
[Django](https://www.djangoproject.com/) with the environment provided by
[Pipenv](https://github.com/pypa/pipenv).

[Docker](https://www.docker.com/) is being used to build this project.

asdf dependencies are listed in the [.tool-versions](.tool-versions) file.

1. Clone this repository

    `$ git clone ssh://git@github.com/jonhue/the_growth_app.git`

2. Install dependencies

    ```
    $ asdf install
    $ pipenv install --dev
    $ pipenv shell

    $ cd frontend
    $ yarn install
    ```

3. Credentials setup

    Duplicate [.env.sample](.env.sample) to `.env`

4. Database setup

    `$ python backend/manage.py migrate`

5. Start development server

    `$ python backend/manage.py runserver`

### Testing

### Deployment

The `master` branch of this repository is automatically deployed on Heroku.

### Error tracking

### Performance tracking
