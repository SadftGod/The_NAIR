import argparse

def parse_args():
    """
        Possible args: 
            *without args : will start Socket thread application server for API connections 
            --teacher : will start script to work with models
            --flask : will start outdated flask server
            --mosquitto: will start script to work with mosquitto service
    """
    parser = argparse.ArgumentParser(description="Will start server or any another module")
    parser.add_argument('--teacher', action='store_true', help="will start script to work with models")
    parser.add_argument('--mosquitto', action='store_true', help="will start script to work with mosquitto service")
    
    return parser.parse_args()
