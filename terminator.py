import boto3
from datetime import datetime, timedelta


# fun that check the format of the date
def check_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        # if the format ok, return true
        return True
    except ValueError:
        # ignore the instances with the wrong format
        print(f"Incorrect date format, should be YYYY-MM-DD. Ignored.")
        # if the format wrong, return false
        return False


# fun that check if the create date longer then a week
def check_instance_age(date_string):
    date_tag = datetime.strptime(date_string, '%Y-%m-%d')
    # if the instance date longer then a week return true else false
    if (datetime.now() - date_tag) > timedelta(weeks=1):
        return True
    else:
        return False


# fun that terminate the instances
def terminate_old_instances():
    # Connect to the EC2 service
    ec2 = boto3.client('ec2')

    # Get a list of all instances
    instances = ec2.describe_instances()['Reservations']

    # Iterate through the instances
    for instance in instances:
        # Check the "Date" tag of the instance
        if 'Tags' in instance['Instances'][0]:
            for tag in instance['Instances'][0]['Tags']:
                # if we are in the right place, key = date, start the checking
                if tag['Key'] == 'Date':
                    date_string = tag['Value']
                    if check_date_format(date_string) and check_instance_age(date_string):
                        instance_id = instance['Instances'][0]['InstanceId']
                        ec2.terminate_instances(InstanceIds=[instance_id])
                        print(f"Instance {instance_id} was terminated.")


def main():
    terminate_old_instances()


main()
