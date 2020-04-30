from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam,
    aws_codecommit as codecommit,
    aws_s3 as s3,
    aws_codebuild as build,
    core
)

class Pipeline(core.Stack):
    def __init__(self, app: core.App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)
        
        # define the inputs and outputs for CodePipeline stages
        source_output = codepipeline.Artifact(artifact_name='SourceOutput')
        cdk_build_output = codepipeline.Artifact("BuildArtifact")
        
        #defining the CodeCommit repo
        repo = codecommit.Repository(self, "Repository",
                    repository_name="cdk-builder-bootcamp",
                    description="cdk-builder-bootcamp"
                )
        
        
        #define the test build project
        cb_test = build.PipelineProject(
            self, "testBuild",
            build_spec=build.BuildSpec.from_source_filename(
                filename='pipeline-infra/buildspecs/cb_test_buildspec.yml'),
            project_name=f"{props['namespace']}-testBuild",
            description='Codepipeline test build system',
            environment=build.LinuxBuildImage.STANDARD_2_0,
            # pass the S3 BucketName into the codebuild project so codebuild knows where to push the package artifact for aws package commands to work
            environment_variables={
                'S3BUCKET': build.BuildEnvironmentVariable(
                    value=props['bucket'].bucket_name)
            }
        )
        
        #define the packaging build project
        cb_package = build.PipelineProject(
            self, "packagingBuild",
            project_name=f"{props['namespace']}-packagingBuild",
            build_spec=build.BuildSpec.from_source_filename(
                filename='pipeline-infra/buildspecs/cb_package_buildspec.yml'),
            description='Codepipeline Packaging build system',
            environment=build.LinuxBuildImage.STANDARD_2_0,
            # pass the S3 BucketName into the codebuild project so codebuild knows where to push the package artifact for aws package commands to work
            environment_variables={
                'S3BUCKET': build.BuildEnvironmentVariable(
                    value=props['bucket'].bucket_name)
            }
        )
        
        # define the CodePipeline
        pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name=f"{props['namespace']}",
            artifact_bucket=props['bucket'],
            stages=[
                codepipeline.StageProps(
                    stage_name='Source',
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            #oauth_token=github_token,
                            #oauth_token=core.SecretValue.plain_text("my-github-token"),
                            #owner="srinivasreddych",
                            repository=repo,
                            action_name='CodeCommit_Source',
                            output=source_output
                        ),
                    ]
                ),
                codepipeline.StageProps(
                    stage_name='Build',
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name='testArtifacts',
                            input=source_output,
                            project=cb_test,
                            run_order=1,
                            #outputs=[cdk_build_output],
                        ),
                        codepipeline_actions.CodeBuildAction(
                            action_name='packageArtifacts',
                            input=source_output,
                            project=cb_package,
                            run_order=2,
                            outputs=[cdk_build_output],
                        )
                    ]
                ),
                codepipeline.StageProps(
                    stage_name='Deploy',
                    actions=[
                        codepipeline_actions.CloudFormationCreateUpdateStackAction(
                            action_name='preReqsDeploy',
                            extra_inputs=[cdk_build_output],
                            stack_name="cdk-builder-bootcamp",
                            run_order=1,
                            admin_permissions=True,
                            #role=props['cfn_role'],
                            template_path=cdk_build_output.at_path(
                                "outputtemplate.yaml"),
                        )
                    ]
                )
            ]
        )
        # give pipelinerole read write to the bucket
        props['bucket'].grant_read_write(pipeline.role)
        # give packageArtifacts Build read write to the bucket
        props['bucket'].grant_read_write(cb_package.role)

        # cfn output
        core.CfnOutput(
            self, "PipelineOut",
            description="Pipeline",
            value=pipeline.pipeline_name
        )
        
        core.CfnOutput(
            self, "CodeCommit",
            description="CodeCommit",
            value=repo.repository_clone_url_http
        )