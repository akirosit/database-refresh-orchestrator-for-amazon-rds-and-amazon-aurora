import boto3
import sys
import json
from botocore.exceptions import ClientError
import logging

if len(sys.argv) != 4:
    print('Usage: python3 launch_refresh.py <application_name> <state_machine_name> <region>')
    print('  Example:')
    print('  python3 launch_refresh.py app1 state-machine-awssol us-east-1')
    print('')
    sys.exit('[Error] Missing or invalid parameters')
else:
    application_name = sys.argv[1]
    state_machine_name = sys.argv[2]
    region = sys.argv[3]
    aws_account_id = boto3.client('sts').get_caller_identity().get('Account')
    
    dbjsondir = "./db-json/" + region
    dbjsonfile = dbjsondir + "/db-" + application_name + ".json"
    state_machine_arn = "arn:aws:states:" + region + ":" + aws_account_id + ":stateMachine:" + state_machine_name
    stepfunctions_client = boto3.client('stepfunctions', region_name=region)

    try:
        with open(dbjsonfile) as json_file:
            sm_input = json.load(json_file)

            response = stepfunctions_client.start_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(sm_input)
            )
        
        print('[OK] Restore initiated')
    except ClientError as e:
        logging.error(e)
        sys.exit('[Error] start_execution API failed')
