#!/usr/bin/env bash

cd $(dirname $0)

pipenv install --dev
pipenv run pytest --ignore vendor