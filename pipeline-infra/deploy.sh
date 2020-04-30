#!/usr/bin/env bash
set -e
set -u
cd $(dirname $0)

#Check utilities are installed or not

cdk_utils=(
  typescript
  aws-cdk
)

check1_cdk_utils=(
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

#Install CDK
install_cdk_utils() {
    for i in ${cdk_utils[*]}; do
        npm install -g $i --force
    done
}

#Check CDK components
check_cdk_utils() {
    for i in ${check1_cdk_utils[*]}; do
        if ! command -v $i > /dev/null 2>&1; then
            echo " The utility $i failed to install and hence exiting" && exit 1
        fi
    done
}

check_nvm
check_node
install_cdk_utils
check_cdk_utils

#Install the required cdk constructs
pip install -r requirements.txt --user
cdk synth
cdk deploy cdk-builder-bootcamp-python-starter-kit --require-approval never
