import boto3
import os
import click

# form the session
session = boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
                        , aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                        , region_name=os.getenv("AWS_DEFAULT_REGION"))

# ec2 resource
ec2 = session.resource("ec2")


def filter_instances(project):
    i_list = []
    if project:
        filters = [{'Name': 'tag:project', 'Values': [project]}]
        i_list = list(ec2.instances.filter(Filters=filters))
    else:
        i_list = list(ec2.instances.all())
        # i_list = [instance for instance in ec2.instances.all()]
    return i_list


@click.group()
def cli():
    """ec2 snappy commands"""


@cli.group('instances')
def instances():
    """Commands for instances"""


@cli.group('volumes')
def volumes():
    """Commands for instance's volumes"""


@cli.group('snapshots')
def snapshots():
    """Commands for volume's snapshots"""


# get the list of instances
@instances.command('list')
@click.option('--project', default=None,
              help="project tag value e.g. --project prj1. if not provided lists all instances")
def list_instances(project):
    """list the instances"""

    i_list = filter_instances(project)

    for i in i_list:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(" , ".join(
            (i.id, i.instance_type, i.placement['AvailabilityZone']
             , i.state['Name'], i.public_dns_name, tags.get('project', '<no-project>'))
        ))

    return


# stop instances
@instances.command('stop')
@click.option('--project', default=None,
              help="project tag value e.g. --project prj1. if not provided stops all instances")
def stop_instances(project):
    """stop the instances"""

    i_list = filter_instances(project)

    for i in i_list:
        if i.state['Name'] == 'running':
            print("Stopping {0} ....".format(i.id))
            i.stop()

    return


# start instances
@instances.command('start')
@click.option('--project', default=None,
              help="project tag value e.g. --project prj1. if not provided starts all instances")
def start_instances(project):
    """start the instances"""

    i_list = filter_instances(project)

    for i in i_list:
        if i.state['Name'] == 'stopped':
            print("Starting {0} ....".format(i.id))
            i.start()

    return


# snap instances
@instances.command('snapshot')
@click.option('--project', default=None,
              help="project tag value e.g. --project prj1. if not provided create snaps of all instances")
def create_snapshots(project):
    """create snapshots of the intended instances"""

    i_list = filter_instances(project)

    for i in i_list:
        for v in i.volumes.all():
            print("Creating snapshot for {0}-{1}".format(i.id,v.id))
            v.create_snapshot(Description="Created by snapshotanalyzer")

    return


# list the volumes of intended instances
@volumes.command('list')
@click.option('--project', default=None,
              help="project tag value of intended ec2 instance e.g. --project prj1. if not provided lists all volumes "
                   "of the all instances")
def list_volumes(project):
    """list the volumes of intended instances"""

    i_list = filter_instances(project)

    for i in i_list:
        for v in i.volumes.all():
            print(" , ".join(
                (
                    i.id
                    , v.id
                    , str(v.size) + " GiB"
                    , v.state
                    , v.volume_type
                    , v.encrypted and "Encrypted" or "Not Encrypted"
                )
            ))

    return


# list the volume's snapshots
@snapshots.command('list')
@click.option('--project', default=None,
              help="project tag value of intended ec2 instance e.g. --project prj1. if not provided lists all "
                   "snapshots of all volumes of the all instances")
def list_snapshots(project):
    """list the snapshots of volumes of intended instances"""

    i_list = filter_instances(project)

    for i in i_list:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(" , ".join(
                    (
                        s.id
                        , v.id
                        , i.id
                        , s.encrypted and "Encrypted" or "Not Encrypted"
                        , s.progress
                        , s.start_time.strftime("%c")
                        , s.state
                        , str(s.volume_size) + " GiB"
                    )
                ))

    return


if __name__ == "__main__":
    cli()
