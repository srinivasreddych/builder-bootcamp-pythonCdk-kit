#!/usr/bin/env bash
set -e
set -u
cd $(dirname $0)

#Check all the required utilities finally
all=(
  nvm
  node
  tsc
  cdk
)

#Install NVM if not present
check_nvm() {
    if ! command -v "nvm" > /dev/null 2>&1; then
        curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash
    fi
}

#Install node if not present
check_node() {
    if ! command -v "node" > /dev/null 2>&1; then
        #Check https://docs.aws.amazon.com/cloud9/latest/user-guide/sample-cdk.html
        nvm install v8.12.0
    fi
}

#Install Typescript if not present
check_install_ts_utils() {
    if ! command -v "tsc" < /dev/null 2>&1; then
        npm install -g "typescript" --force
    fi
}

#Install CDK if not present
check_install_cdk_utils() {
    if ! command -v "cdk" < /dev/null 2>&1; then
        npm install -g "aws-cdk" --force
    fi
}

check_nvm
check_node
check_install_ts_utils
check_install_cdk_utils

#Install the required cdk constructs
pip3 install -r requirements.txt --user
cdk synth
cdk deploy cdk-builder-bootcamp-python-starter-kit --require-approval never
