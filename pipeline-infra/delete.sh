#!/usr/bin/env bash
set -e
set -u
cd $(dirname $0)

cdk destroy cdk-builder-bootcamp-python-starter-kit --force