#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
import optparse, json, yaml
import os,config
import logging, logging.config

from dpserv_uplink import dpserv_uplink
from dpserv_output import dpserv_output

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

with open('./logging.conf','r') as f:
    logConf = yaml.load(f)
logging.config.dictConfig(logConf)
logger = logging.getLogger('dpservClient')

##################################################################### MAIN STUFF
################################################################################
def main():
    logger.info("dpserv_client started")
    ############ Handle input & parameters
    p = optparse.OptionParser()
    p.add_option('--url', '-u', action="store", default=None, help="Service root URL")
    p.add_option('--collection','-c', action="store", default="all", help="Collection to use (default: all)")
    p.add_option('--document', action="store", default=None, help="Document ID to consult")
    p.add_option('--list_collections','-l',action="store_true",dest="listCollections",default=False, help="List collections")
    p.add_option('--parameters','-p',action="store",default=[], help="Optional collection parameters, in json")
    p.add_option('--json_out','-j',action="store_true",default=False, help="Output JSON")
    p.add_option('--dir_out','-d',action="store",default=None,help="Output directory")
    p.add_option('--include','-i',action="append",dest="related_files",help="Include related documents")
    p.add_option('--meta','-m',action="store_true",default=False,help="Only output meta (no binary/text content)")
    p.add_option('--output',action="store",default="text",help="")
    options, arguments = p.parse_args()

    if not options.url:
        p.error('Service url not defined')

    if options.parameters:
        options.parameters = json.loads(options.parameters)


    logger.info("Accessing {0}, collection {1} (parameters: {2}) Json: {3} Dir: {4} Include: {5}".format(
                 options.url
                ,options.collection
                ,options.parameters
                ,options.json_out
                ,options.dir_out
                ,options.related_files))

    ############ Retrieve data
    uplink = dpserv_uplink()
    output = dpserv_output(options)

    if options.document:
        data = uplink.use_service(options.url) \
                     .find_document(options.document) \
                     .get_document()

        if not options.meta:
                data["content"] = uplink.get_content(options.output)

        output.msg("Output for %s:" % options.document) \
              .content(data) \
              .stdout()

    elif options.listCollections:
        data = uplink.use_service(options.url) \
                     .get_collections()
        output.msg("List of available collections:") \
              .content(data) \
              .stdout()
    else:
        docList = uplink.use_service(options.url) \
                        .use_collection(options.collection, options.parameters) \
                        .get_documents()
        for doc in docList:
            data = uplink.use_document(doc).get_document()
            output.msg("Info for doc %s" % data["id"]) \
                  .content(data) \
                  .stdout()

    return None

########################################################################### INIT
################################################################################
if __name__ == '__main__':
  try:
      main()
  except Exception:
    logger.exception('dpserv_client general exception')
    raise
