## Uplink module
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
import requests, logging
logger = logging.getLogger('dpservClient')

class dpserv_uplink:
    _data = []
    _collections = []
    _collection = []

    def __init__(self):
        return None

    #################### API
    ########################
    def use_service(self,Url):
        self._data = self._getJson(Url)
        return None

    def list_collections(self,serviceUrl):
        return None

    def use_collection(self,collection,parameters=[]):
        ColsUrl = self._getLink(self._data, "collections")
        self._collections = self._getJson(ColsUrl)
        ColUrl = self._getLink(self._collections,collection)
        self._collection = self._getJson(ColUrl,parameters)
        return None

    def documents(self):
        colUrl = self._collections_url(self._serviceurl)


        return None

    def document(self,docUrl):
        return None

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
    def collection_url(self, data, collection):
        for link in data["links"]:
            if link["rel"] == collection:
                return link["href"]
        raise IndexError("Link to collection {0} cannot be found.".format(collection))

    def _collections_url(self, data):
        for link in data["links"]:
            if link["rel"] == "collections":
                return link["href"]
        raise IndexError("Link to collections cannot be found.")

    def _getLink(self, data, element):
        for link in data["links"]:
            if link["rel"] == element:
                return link["href"]
        raise IndexError("Link to {0} cannot be found.".format(element))

    def _getJson(self,Url,Params=None):
        logger.debug("Uplink accessing {0} ({1})".format(Url,Params))
        rs = requests.get(Url, params=Params)
        if rs.status_code != 200:
            raise ApiError('GET {0} {1}'.format(serviceUrl,rs.status_code))
        return rs.json()
