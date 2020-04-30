#!/usr/bin/env bash

cd $(dirname $0)

# vendor python dependencies
rm -rf vendor
pipenv lock -r > req.txt
pipenv run pip install -r req.txt -t ./vendor
rm req.txt