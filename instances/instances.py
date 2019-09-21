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
def instances():
    """Commands for instances"""


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


if __name__ == "__main__":
    instances()
