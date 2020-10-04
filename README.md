# snapshot

demo ec2 project
## about

demo for setting up boto3  to manager ec2

## configuring

shotty uses configfile for the aws cli

`aws configure --profile shotty`

## Running

`pipenv run python "shotty/shotty.py" <command> <--project=Project>`

*command* is instances, volumes, or snapshots
*subcommand* - depends on command
*project* is optional
