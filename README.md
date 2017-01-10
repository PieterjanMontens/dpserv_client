# dpserv_client
*work in progress*

Auto-discovering import client for [dpserv](https://github.com/RvS-CdE/dpserv) document server, able to navigate the server API from the root URL on.

## Current state

 * Discovers and follows links provided by dpserv
 * Exports meta and content in json format
 * Can use client private key
 * Inclusion of optional related files (project, translation)

## Technology

 * Python3

## Todo

 * Auto-export whole collections
 * Apply session limits to avoid being blocked

## Usage

 * Clone repository
 * Make src/dpserv_client.py executable (or execute with python3)
 * Point script to dpserv root URL and provide parameters

### Examples
List available collections:

    ./dpserv_client.py -u http://www.raadvst-consetat.be/dbx/avis --list_collections

Particular document meta-data:

    ./dpserv_client.py -u http://www.raadvst-consetat.be/dbx/avis --document 52060 --meta

Document with metadata, content and german translation, in JSON format:

    ./dpserv_client.py -u http://www.raadvst-consetat.be/dbx/avis --document 56372 --include german_translation
 
