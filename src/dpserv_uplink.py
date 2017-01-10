## Uplink module
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
import requests, logging
logger = logging.getLogger('dpservClient')

class dpserv_uplink:
    _key = ''
    _data = []
    _collections = []
    _collection = []

    _ctype2mime = {'text'   : 'text/plain'
                  ,'html'   : 'text/html'
                  ,'pdf'    : 'application/pdf'
                  }

    def __init__(self):
        return None

    #################### API
    ########################
    def use_key(self, Key):
        self._key = Key
        return self

    def use_service(self,Url):
        self._data = self._getJson(Url)
        return self

    def use_collection(self,collection,parameters={}):
        ## TODO: make a nice object of this so I could just chain methods cleanly
        ColsUrl = self._getLink(self._data["links"], "collections")
        self._collections = self._getJson(ColsUrl)
        ColData = self._getContentById(self._collections["content"],collection)
        ColUrl = self._getLink(ColData["links"],"self")
        self._collection = self._getJson(ColUrl,parameters)
        return self

    def use_document(self,docDef):
        DocUrl = self._getLink(docDef["links"],"self")
        self._doc = self._getJson(DocUrl)
        return self

    def get_documents(self):
        return self._collection["content"]

    def get_document(self):
        return self._doc

    def find_document(self,docid):
        MaskDef = self._getContentById(self._data["content"],"document_url_mask")
        DocUrl = MaskDef["url_template"].replace(MaskDef["placeholder"], docid)
        self._doc = self._getJson(DocUrl)
        return self

    def get_collections(self):
        ColsUrl = self._getLink(self._data["links"], "collections")
        self._collections = self._getJson(ColsUrl)
        return self._collections["collections"]

    def get_content(self,ctype="text",rel="content"):
        Mime = self._ctype2mime[ctype]
        ContUrl = self._getLink(self._doc["links"], rel)
        return self._getFile(ContUrl,Mime)

    def dump(self):
        print("Root data:")
        print(self._data)
        print("Collections data:")
        print(self._collections)
        print("Collection data:")
        print(self._collection)
        return None

    ############### INTERNAL
    ########################
    def _getLink(self, data, needle):
        for link in data:
            if link["rel"] == needle:
                return link["href"]
        raise IndexError("Link to {0} cannot be found.".format(needle))

    def _getContentById(self, data, needle):
        for content in data:
            if content["id"] == needle:
                return content
        raise IndexError("Content id {0} cannot be found.".format(needle))

    def _getJson(self,Url,Params={}):
        logger.debug("Uplink accessing {0} ({1})".format(Url,Params))
        Params['api_key'] = self._key
        rs = requests.get(Url, params=Params)
        if rs.status_code != 200:
            logger.error("Error {0} in accessing {1}".format(rs.status_code,Url))
            return {}
        return rs.json()

    def _getFile(self,Url,Accept):
        logger.debug("Obtaining file from {0} in {1}".format(Url,Accept))
        headers = {'accept': Accept}
        params = {'api_key' : self._key}
        rs = requests.get(Url, headers=headers, params=params)
        if rs.status_code != 200:
            logger.error("Error {0} in accessing {1}".format(rs.status_code,Url))
            raise Exception("Error {0} in accessing {1}".format(rs.status_code,Url))
            return ''
        return rs.text

