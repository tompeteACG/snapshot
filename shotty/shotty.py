import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):

    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """shotty managers snapshots"""

@cli.group('snapshots')
def snapshots():
    """commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
    help = "only snapshots for project (tag Project:<name>)")

def list_snapshots(project):
    "list ec2 snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return


@cli.group('volumes')
def volumes():
      """commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
    help = "only volumes for project (tag Project:<name>)")

def list_volumes(project):
    "list ec2 volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
            v.id,
            i.id,
            v.state,
            str(v.size) + "GiB",
            v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@cli.group('instances')
def instances():
    """Commande for instances"""


@instances.command('snapshot',
    help="create snapshot of all volumes")
@click.option('--project', default=None,
    help = "only instances for project (tag Project:<name>)")
def list_snapshots(project):
    "create snapshots for ec2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Snapshot...")

        print("Starting {0}...".format(i.id))

        i.start()
        i.wait_until_running()

    print("job's done")
    return

@instances.command('list')
@click.option('--project', default=None,
    help = "only instances for project (tag Project:<name>)")

def list_instances(project):
    "list ec2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

    return


@instances.command('stop')
@click.option('--project', default=None,
    help='only instances for project')
def stop_instances(project):
    "stop ec2 instances"


    instances = filter_instances(project)

    for i in instances:
        print("stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
    help='only instances for project')
def start_instances(project):
    "start ec2 instances"


    instances = filter_instances(project)

    for i in instances:
        print("starting {0}...".format(i.id))
        i.start()

    return



if __name__ == '__main__':
    cli()
