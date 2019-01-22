import boto.ec2
import time
import os
import csv
import paramiko

def get_key(conn):

    """ Try creating a new key_pair. If key_pair already exits, there will be
        an error. """

    try:
        key_pair = conn.create_key_pair('my_key')
        key_pair.save("")
    # if there is an error (key_pair already exits), get existing key_pair
    except boto.exception.EC2ResponseError:
        key_pair = 'my_key'

    return key_pair

def get_security_group(conn):

    """ Try creating a new security group. If security group already exits,
        there will be an error. """

    try:
        security_group = conn.create_security_group('csc326-group24',
                        'security group for csc326')
        security_group.authorize('icmp', -1, -1, '0.0.0.0/0')
        security_group.authorize('tcp', 22, 22, '0.0.0.0/0')
        security_group.authorize('tcp', 80, 80, '0.0.0.0/0')
    # if there is an error, get existing security group
    except boto.exception.EC2ResponseError:
        security_group = 'csc326-group24'

    return security_group

def aws_setup():

    """ This function connects to us-east-1, sets up an instance,
        copys files to the instance, and starts the server. """

    aws_access_key_id = ''
    aws_secret_access_key = ''

    # read csv file
    csv_file = open('credentials.csv')
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        aws_access_key_id = row['Access key ID']
        aws_secret_access_key = row['Secret access key']
        break

    ami = 'ami-9aaa1cf2'

    # setup connection
    conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id =
        aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

    key_pair = get_key(conn)

    security_group = get_security_group(conn)

    # start instance
    print ('Starting instance...')
    resp = conn.run_instances(
        ami, instance_type = 't2.micro', key_name = 'my_key',
        security_groups = ['csc326-group24'])

    inst = resp.instances[0]

    while inst.update() != 'running':
        time.sleep(1)

    # get instance id
    instance_id = inst.id
    instance_id = instance_id.encode('ascii')
    print ('Instance ID: ', instance_id)

    # get ip address
    address = conn.allocate_address()
    address.associate(instance_id)
    ip = address.public_ip
    ip = ip.encode('ascii')
    print ('Public IP: ', ip)

    # get dns of the instance (instance_id)
    dns = inst.public_dns_name
    dns = dns.encode('ascii')
    print ('Public DNS: ', dns)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        print("Trying to connect...")
        try:
            ssh.connect(hostname = str(ip), username = "ubuntu", timeout = 25.0,
            key_filename = "my_key.pem")
            break
        except Exception:
            print("Trying again...")

    print("Connected!")

    stdin, stdout, stderr = ssh.exec_command('sudo apt-get purge openssh-server')
    stdin, stdout, stderr = ssh.exec_command('sudo apt-get install openssh-server')

    # Copy folder to AWS virtual machine
    os.system('chmod 400 my_key.pem')
    while True:
        print("Copying folder to AWS virtual machine...")
        try:
            os.system('scp -i my_key.pem -o StrictHostKeyChecking=no -r' + ' ' +
            'lab4_group_24.tar.gz ubuntu@' + str(ip) + ':~/')
            break
        except Exception:
            print("Trying again...")

    print("Done!")

    print("Installing packages...")
    # install packages and run frontend.py
    commands = ['sudo apt-get update',
                'sudo apt-get install --yes python-pip',
                'sudo pip install bottle',
                'sudo pip install beaker',
                'sudo pip install redis',
                'sudo pip install autocorrect',
                'sudo pip install oauth2client',
                'sudo pip install google-api-python-client',
                'tar -xf lab4_group_24.tar.gz',
                'cd GoogleSearchEngine-master \n screen -d -m sudo python frontend.py']

    for command in commands:
        print (command)
        stdin, stdout, stderr = ssh.exec_command(command)
        print (stdout.read())

    print ('Go to  http://' + str(ip) + ':80/ or http://' + str(dns))


if __name__ == '__main__':
    aws_setup()
