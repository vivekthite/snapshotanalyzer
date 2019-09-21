# snapshotanalyzer
Demo project in python to manage AWS EC2 instances snapshots

## Prerequisite
python 3

## Running
1) `pipenv install' #Note: This should be run only once after checkout
2) `pipenv run python instances/instances.py <COMMAND> <OPTIONS>`
            <br/>COMMAND : start/stop/list
            <br/>OPTIONS : --project (it is optional)
        <br/><p>Note: to get help try => `pipenv run python instances/instances.py --help`
                                  or  `pipenv run python instances/instances.py <command> --help`

         e.g.
            $ pipenv run python instances/instances.py --help
                Usage: instances.py [OPTIONS] COMMAND [ARGS]...

                  Commands for instances

                Options:
                  --help  Show this message and exit.

                Commands:
                  list   list the instances
                  start  start the instances
                  stop   stop the instances

            ==================================

            $ pipenv run python instances/instances.py start --help
                Usage: instances.py start [OPTIONS]

                  start the instances

                Options:
                  --project TEXT  project tag value e.g. --project prj1. if not provided
                                  starts all instances
                  --help          Show this message and exit.

            ============================================

            $ pipenv run python instances/instances.py list
                i-0dcfdb4616465c4ab , t2.micro , us-east-1b , running , ec2-18-212-66-28.compute-1.amazonaws.com , <no-project>
                i-0d39a9250741f53e8 , t2.micro , us-east-1b , running , ec2-52-23-162-247.compute-1.amazonaws.com , prj1

            =================================================

            $ pipenv run python instances/instances.py list --project prj1
                i-0d39a9250741f53e8 , t2.micro , us-east-1b , running , ec2-52-23-162-247.compute-1.amazonaws.com , prj1

            ================================================

