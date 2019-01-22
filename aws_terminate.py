import boto.ec2
import sys
import csv

def aws_terminate():

    """ This function connects to us-east-1 and terminates the instance. """

    aws_access_key_id = ''
    aws_secret_access_key = ''

    # read csv file
    csv_file = open('credentials.csv', newline='')
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        aws_access_key_id = row['Access key ID']
        aws_secret_access_key = row['Secret access key']
        break

    # get instance id
    if len(sys.argv) != 2:
        print ("Error!")
        print ("Please enter:")
        print ("python aws_terminate.py <instance_id>")
        sys.exit()

    instance_id = sys.argv[1]

    # setup connection
    conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id =
        aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

    conn.terminate_instances(instance_ids = [instance_id])

    print ('Instance terminated!')

if __name__ == '__main__':
    aws_terminate()
