# cloudigrade

[![license](https://img.shields.io/github/license/cloudigrade/cloudigrade.svg)]()
[![Build Status](https://travis-ci.org/cloudigrade/cloudigrade.svg?branch=master)](https://travis-ci.org/cloudigrade/cloudigrade)
[![codecov](https://codecov.io/gh/cloudigrade/cloudigrade/branch/master/graph/badge.svg)](https://codecov.io/gh/cloudigrade/cloudigrade)
[![Updates](https://pyup.io/repos/github/cloudigrade/cloudigrade/shield.svg)](https://pyup.io/repos/github/cloudigrade/cloudigrade/)
[![Python 3](https://pyup.io/repos/github/cloudigrade/cloudigrade/python-3-shield.svg)](https://pyup.io/repos/github/cloudigrade/cloudigrade/)

# What is cloudigrade?

**cloudigrade** is an open-source suite of tools for tracking Linux distribution
use (although chiefly targeting RHEL) in public cloud platforms. **cloudigrade**
actively checks a user's account in a particular cloud for running instances,
tracks when instances are powered on, determines what Linux distributions are
installed on them, and provides the ability to generate reports to see how
long different distributions have run in a given window.

## What is this "Doppler" I see referenced in various places?

Doppler is another code name for **cloudigrade**.

Or is **cloudigrade** a code name for Doppler?

`cloudigrade == Doppler` for all intents and purposes. 😉


# Running cloudigrade

We do not yet have concise setup notes for running **cloudigrade**, and we currently require setting up a complete development envirionment. Watch this space for changes in the future, but for now, please read the next "Developer Environment" section.

## Developer Environment


Because **cloudigrade** is actually a suite of interacting services, setting up a development environment may require installing some or all of the following dependencies:

- Python (one of the versions we support)
- [Docker](https://www.docker.com/community-edition#/download)
- [docker-compose](https://docs.docker.com/compose/install/)
- [tox](https://tox.readthedocs.io/)
- [gettext](https://www.gnu.org/software/gettext/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [AWS Command Line Interface](https://aws.amazon.com/cli/)


### macOS dependencies

We encourage macOS developers to use [homebrew](https://brew.sh/) to install and manage these dependencies. The following commands should install everything you need:

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew update
    brew install python pypy3 gettext awscli postgresql
    brew link gettext --force
    brew cask install docker


### Python virtual environment

We strongly encourage all developers to use a virtual environment to isolate **cloudigrade**'s Python package dependencies. You may use whatever tooling you feel confortable with, but here are some initial notes for setting up with [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper):

    # install virtualenv and virtualenvwrapper
    pip install -U pip
    pip install -U virtualenvwrapper virtualenv
    echo "source \"$(brew --prefix)/bin/virtualenvwrapper.sh\"" >> ~/.bash_profile
    source $(brew --prefix)/bin/virtualenvwrapper.sh

    # create the environment
    mkvirtualenv cloudigrade

    # activate the environment
    workon cloudigrade

Once you have an environment set up, install our Python package requirements:

    pip install -U pip wheel tox
    pip install -r requirements/local.txt


### Configure AWS account credentials

If you haven't already, create an [Amazon Web Services](https://aws.amazon.com/) account for **cloudigrade** to use for its AWS API calls. You will need the AWS access key ID, AWS secret access key, and region name where the account operates.

Use the AWS CLI to save that configuration to your local system:

    aws configure

You can verify that settings were stored correctly by checking the files it created in your `~/.aws/` directory.

AWS access for running **cloudigrade** inside Docker must be enabled via environment variables. Set the following variables in your local environment *before* you start running in Docker containers. Values for these variables can be found in the files in your `~/.aws/` directory.

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`


### Configure Django settings module

For convenience, you may want to set the following environment variable:

    DJANGO_SETTINGS_MODULE=config.settings.local

If you do not set that variable, you may need to include the `--settings=config.settings.local` argument with any Django admin or management commands you run.


## Common commands

### Running

To run the application along with the postgres database and queue
run the following:

    make start-compose

If you would like to run just the database, so you can run the application
on your local machine, use the following command:

    make start-db

To reinstantiate the docker psql db, run the following:

    make reinitdb

If you would like to run just the queue, so you can interact with the queue on
your local machine, use the following command:

    make start-queue

### Testing

To run all local tests as well as our code-quality checking commands:

    tox

If you wish to run _only_ the tests:

    make unittest

If you wish to run a higher-level suite of integration tests, see
[integrade](https://github.com/cloudigrade/integrade).


### Authentication

Django Rest Framework token authentication is used to authenticate users. API
access is restricted to authenticated users. All API calls require an
Authorization header:

    Authorization: "Token `auth_token`"

To create a user run the following make command and follow the prompts:

    make user

To then generate an auth token, run the make command:

    make user-authenticate

This auth token can be supplied in the Authorization header.

### Message Broker

RabbitMQ is used to broker messages between **cloudigrade** and inspectigrade
services. There are multiple Python packages available to interact with
RabbitMQ; the officially recommended packaged is [Pika](https://pika.readthedocs.io/en/latest/). Both services serve as producers and consumers of the message queue.
The **cloudigrade** docker-compose file requires that a password environment
variable be set for the RabbitMQ user. Make sure that the following has been
set in your local environment before starting

    RABBITMQ_DEFAULT_PASS

The RabbitMQ container can persist message data in the **cloudigrade** directory.
To purge this data use

    make remove-compose-queue
