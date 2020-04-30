#!/usr/bin/env python3

from aws_cdk import core

from pipeline_modules.cicd_stack import Pipeline
from pipeline_modules.pre_reqs import PreReqs


props = {'namespace': 'cdk-builder-bootcamp', 
         'AWS_ACCOUNT_ID': core.Aws.ACCOUNT_ID, 
         'AWS_DEFAULT_REGION': core.Aws.REGION
}

app = core.App()
env = core.Environment(account="560360184571", region="us-west-2")

prereqs=PreReqs(app, "pre-reqs", props, env=env)

pipeline=Pipeline(app, "cdk-builder-bootcamp-python-starter-kit", prereqs.outputs, env=env)
pipeline.add_dependency(prereqs)

app.synth()
