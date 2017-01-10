# dpserv_client
*work in progress*

Auto-discovering import client for dpserv document server, able to navigate the server API from the root URL on.

## Current state

 * Discovers and follows links provided by dpserv
 * Exports meta and content in json format
 * Can use client private key

## Technology

 * Python3

## Todo

 * Auto-export whole collections
 * Apply session limits to avoid being blocked

## Usage

 * Clone repository
 * Make src/dpserv_client.py executable (or execute with python3)
 * Point script to root URL and provide parameters

### Examples
List available collections:

    python3 dpserv_client.py -u http://www.raadvst-consetat.be/dbx/avis --list_collections

Particular document meta-data:
    python3 dpserv_client.py -u http://www.raadvst-consetat.be/dbx/avis --document 52060 --meta

Document with content and all, in json format:
    python3 dpserv_client.py -u http://www.raadvst-consetat.be/dbx/avis --document 52060
 
