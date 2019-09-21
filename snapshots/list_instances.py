import boto3
import os
import click

# form the session
session = boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
                        , aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                        , region_name=os.getenv("AWS_DEFAULT_REGION"))

# ec2 resource
ec2 = session.resource("ec2")


# get the list of instances
@click.command()
def list_instances():
    """list the all instances"""
    i_list = list(ec2.instances.all())
    # i_list = [instance for instance in ec2.instances.all()]
    print(i_list)
    message="instance={0} , id={1} , type={2} , zone={3} , state={4} , public dns={5}"
    print(message.format(i_list[0],i_list[0].id
                         ,i_list[0].instance_type,i_list[0].placement['AvailabilityZone']
                         ,i_list[0].state['Name'],i_list[0].public_dns_name))
    return i_list


if __name__ == "__main__":
    list_instances()
