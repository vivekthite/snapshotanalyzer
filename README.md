# snapshotanalyzer
Demo project in python to manage AWS EC2 instances snapshots

## Prerequisite
python 3

## Running
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
                
                           
                          
                      

