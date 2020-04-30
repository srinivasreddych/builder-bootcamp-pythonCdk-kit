from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam,
    aws_codecommit as codecommit,
    aws_s3 as s3,
    aws_codebuild as build,
    core
)

class PreReqs(core.Stack):
    def __init__(self, app: core.App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)
        
        #CP S3 bucket
        bucket = s3.Bucket(
            self, "ArtifactBucket",
            bucket_name=f"{props['namespace'].lower()}-{'cp'}-{core.Aws.ACCOUNT_ID}",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY)
        
        
       
        #CFN Deployer role
        cfn_role = iam.Role(self, "Role",
                        assumed_by=iam.CompositePrincipal(
                            iam.ServicePrincipal('cloudformation.amazonaws.com'),
                            iam.AccountPrincipal('560360184571')))
        
        cfn_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["cloudformation:*","lambda:*", "iam:*", "apigateway:*", "dynamodb:*"],
            resources=["*"]
        ))
        
        
        
        self.output_props = props.copy()
        self.output_props['bucket']= bucket
        self.output_props['cfn_role']= cfn_role

    # pass objects to another stack
    @property
    def outputs(self):
        return self.output_props
