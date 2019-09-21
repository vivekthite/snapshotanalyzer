import boto3
import os


def get_instances():
    client = boto3.client(
        'ec2',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    boto3.session()
    response = client.describe_instances()
    i_list = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]
    return i_list

if __name__ == "__main__":
    print(get_instances())
