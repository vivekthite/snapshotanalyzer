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


def has_pending_snapshots(volume):
    snaps = list(volume.snapshots.all())
    return snaps and snaps[0].state == 'pending'


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
        else:
            print("Could not stop {0} as it's state is {1}".format(i.id, i.state['Name']))

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
        else:
            print("Could not start {0} as it's state is {1}".format(i.id, i.state['Name']))

    return


# snap instances
@instances.command('snapshot')
@click.option('--project', default=None,
              help="project tag value e.g. --project prj1. if not provided create snaps of all instances")
def create_snapshots(project):
    """create snapshots of the intended instances"""

    i_list = filter_instances(project)

    for i in i_list:
        print("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            if has_pending_snapshots(v):
                print('Skipping {0} , snapshot is in progress'.format(v.id))
                continue
            print("Creating snapshot for {0}... : {1}".format(i.id, v.id))
            snap = v.create_snapshot(Description="Created by snapshotanalyzer")
            """
                No need to wait to complete the snapshot. u can immediately
                return and start the instance. It is safe and best practice.
            """
            # snap.wait_until_completed()
            # snap.load()
            # print("Snapshot of {0} : {1} is {2}".format(i.id, v.id, snap.state))
        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running()
        print("Snapshot Job Done. Hurray :) !")
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
@click.option('--all','list_all',default=False,is_flag=True,help='lists all snapshots')
def list_snapshots(project,list_all):
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
                # snapshots are returned in most recent first
                # show only most recent completed snapshots.
                if s.state == 'completed' and not list_all: break

    return


if __name__ == "__main__":
    cli()
