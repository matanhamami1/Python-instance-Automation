# Create Ec2 instance using Python BOTO3
import boto3
import datetime

current_date = ""


# fun that return tuple with the values to create a instance
def instance_values():
    # open the configuration file and paste the details
    with open(r"C:\Users\devops\Downloads\configuration.txt", "r") as file:
        # open the configuration file and paste the details
        config = file.read().splitlines()
        instance_type = config[0].split(":")[1]
        key_name = config[1].split(":")[1]
        image_id = config[2].split(":")[1]
        security_group = config[3].split(":")[1].replace("[", "").replace("]", "").replace("\"", "").split(",")
        values_tuple = (instance_type, key_name, image_id, security_group)
    return values_tuple


def create_ec2_instance(number_of_instances):
    """
    :param number_of_instances: number of instance to create
    :return: print the output "instance web " + str(i+1) + " created"
    and the private ip of the instance
    """
    try:
        print("Creating Ec2 instance, enter")
        resource_ec2 = boto3.client("ec2")
        instances = []
        # with current_date we add date tag to the instance
        global current_date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        for i in range(number_of_instances):
            # open the file user-data.sh to run the recommend install httpd and add sentence
            sentence = input("enter your sentence: ")
            with open(r"C:\Users\devops\Downloads\user-data.sh", "r") as file:
                user_data = file.read()
                # put the input sentence
                user_data = user_data.replace("SENTENCE_PLACEHOLDER", sentence)
                # create the instance
                # put in tuple the instance_values()'s return
            tuple_with_instance_values = instance_values()
            response = resource_ec2.run_instances(
                InstanceType=tuple_with_instance_values[0],
                KeyName=tuple_with_instance_values[1],
                ImageId=tuple_with_instance_values[2],
                SecurityGroupIds=tuple_with_instance_values[3],
                MinCount=1,
                MaxCount=1,
                UserData=user_data,
                # change the instance name and the tag date
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                # add name
                                'Key': 'Name',
                                'Value': 'web' + str(i + 1)
                            },
                            {
                                # add date
                                'Key': 'Date',
                                'Value': current_date
                            },
                        ]
                    },
                ]
            )
            # add the instance to list and print the web that created
            instances.append(response['Instances'][0]['InstanceId'])
            print("instance web " + str(i + 1) + " created")
        describe_ec2_instance(instances)

    except Exception as e:
        print(e)


# Modify the describe_ec2_instance function to take a list of instance ids
def describe_ec2_instance(instance_ids):
    """
    print the private ip of the instance
    :return:
    """
    try:
        resource_ec2 = boto3.client("ec2")
        response = resource_ec2.describe_instances(InstanceIds=instance_ids)
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                print("Private IP address of instance " + instance["InstanceId"] + ": " + instance["PrivateIpAddress"])
    except Exception as e:
        print(e)


def main():
    number_of_instances = input("enter the number of instance you want to create: ")
    create_ec2_instance(int(number_of_instances))


main()


