## Output module
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
import sys,logging
import json, yaml
logger = logging.getLogger('dpservClient')

class dpserv_output:
    _meta = False
    _output = "yaml"
    _msg = ""
    _cnt = None

    def __init__(self,options={}):
        if (options.json_out):
            self._output = "json"
        #if (options.meta)
        #    self._meta = True
        return None

    #################### API
    ########################
    def msg(self,text):
        self._msg = text
        return self

    def content(self,cnt):
        self._cnt = cnt
        return self

    def get(self):
        Out = self._get_output()
        if self._output == "json":
            return json.dumps(self._get_output())
        if self._output == "yaml":
            return yaml.dump(self._get_output())
        return Out

    def stdout(self,msg=None):
        if msg is None:
            msg = self.get()

        sys.stdout.write(msg)
        return None

    ############### INTERNAL
    ########################
    def _get_output(self):
        return {'msg' : self._msg
               ,'payload' : self._cnt}

