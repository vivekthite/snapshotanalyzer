# snapshotanalyzer
Demo project in python to manage AWS EC2 instances snapshots

## Prerequisite
python 3

## Environment variables to export
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

## Running - End User
1) pipenv run python setup.py bdist_wheel
2) ec2 --help

    e.g. 
        $ ec2 --help
            Usage: ec2 [OPTIONS] COMMAND [ARGS]...
            
              ec2 snappy commands
            
            Options:
              --help  Show this message and exit.
            
            Commands:
              instances  Commands for instances
              snapshots  Commands for volume's snapshots
              volumes    Commands for instance's volumes
 
## For DEV - Running
1) `pipenv install' #Note: This should be run only once after checkout
2) `pipenv run pipenv run python scripts/ec2.py <COMMAND> <SUBCOMMAND> <OPTIONS>`
            <br/>COMMAND : instances/volumes/snapshots
            <br/>SUBCOMMAND : dependes upon COMMAND. e.g. list/start/stop/snapshot etc
            <br/>OPTIONS : --project (it is optional)
        <br/><p>Note: to get help try => `pipenv run pipenv run python scripts/ec2.py --help`
                                  or  `pipenv run pipenv run python scripts/ec2.py <command> --help`

         
            e.g. 
                $ pipenv run python scripts/ec2.py --help
                    Usage: ec2.py [OPTIONS] COMMAND [ARGS]...
                    
                      ec2 snappy commands
                    
                    Options:
                      --help  Show this message and exit.
                    
                    Commands:
                      instances  Commands for instances
                      snapshots  Commands for volume's snapshots
                      volumes    Commands for instance's volumes
                ===================================================
                
                $ pipenv run python scripts/ec2.py instances --help
                    Usage: ec2.py instances [OPTIONS] COMMAND [ARGS]...
                    
                      Commands for instances
                    
                    Options:
                      --help  Show this message and exit.
                    
                    Commands:
                      list      list the instances
                      snapshot  create snapshots of the intended instances
                      start     start the instances
                      stop      stop the instances
                =======================================================
                
                
                $ pipenv run python scripts/ec2.py instances list --help
                    Usage: ec2.py instances list [OPTIONS]
                    
                      list the instances
                    
                    Options:
                      --project TEXT  project tag value e.g. --project prj1. if not provided lists
                                      all instances
                      --help          Show this message and exit.  
                ===========================================================
                
                
                $ pipenv run python scripts/ec2.py instances list
                    i-0dcfdb4616465c4ab , t2.micro , us-east-1b , running , ec2-18-212-66-28.compute-1.amazonaws.com , <no-project>
                    i-0d39a9250741f53e8 , t2.micro , us-east-1b , running , ec2-3-95-132-159.compute-1.amazonaws.com , prj1  
                =====================================================================
                
                
                $ pipenv run python scripts/ec2.py instances list --project prj1
                    i-0d39a9250741f53e8 , t2.micro , us-east-1b , running , ec2-3-95-132-159.compute-1.amazonaws.com , prj1 
                =====================================
                
## TODOs
    1. Add the ability to “reboot” instances.
    2. Add a “—force” flag to the “instances stop”, “start”, “snapshot”, and
    “reboot” commands.
        a. If “—project” isn’t set, exit the command immediately with an
        error message, unless “—force” is set.
    3. Add a “—profile” option to the “cli” group, which let’s you specify a
    different profile.
        e.g. “shotty —profile Kyle instances stop —force”
    4. Use a try/except block to catch “botocore.exceptions.ClientError”
        when creating snapshots, and print an error message.
    5. Add an “instance” argument to the appropriate commands, so
        they only target one instance.
        e.g. “shotty volumes list —instance=i-0123456789abcdef”
    6. After a snapshot, only start instances that were running before
        the snapshot was taken.  
    7. Add an optional “age” parameter to the “snapshot” command that
        takes an age in days and only snapshots volumes whose last
        successful snapshot is older than that many days.
        e.g. “shotty instances snapshot —age 7 —project Valkyrie”
    8. When snapshotting, don’t stop an instance unless the script will
        snapshot one of its volumes.
    9. Add a “region” parameter to all commands that will let the user
        override the region set in their AWS CLI configuration profile.
        e.g. “shotty —region us-east-1 instances list”                                 
                              
                      

