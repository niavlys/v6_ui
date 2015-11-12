from shapely.geometry import asShape
from shapely.ops import transform
from functools import partial
import httplib2
import pyproj
import json

from pyramid.httpexceptions import (
    HTTPBadRequest, HTTPNotFound, HTTPInternalServerError)

from c2corg_common.attributes import default_cultures


class Document(object):

    # FIXME Is a "documents" route available/relevant in the API?
    _API_ROUTE = 'documents'

    def __init__(self, request):
        self.request = request
        self.settings = request.registry.settings
        self.template_input = {
            'debug': 'debug' in self.request.params,
            'api_url': self.settings['api_url']
        }

    def _call_api(self, url, method='GET', body=None, headers=None):
        http = httplib2.Http()
        try:
            resp, content = http.request(
                url, method=method, body=body, headers=headers
            )
            return resp, json.loads(content)
        except Exception:
            # TODO: return error message as the second item
            return {'status': '500'}, {}

    def _validate_id_culture(self):
        if 'id' not in self.request.matchdict:
            # eg. creating a new document
            return None, None
        try:
            id = int(self.request.matchdict['id'])
        except Exception:
            raise HTTPBadRequest("Incorrect id")

        culture = str(self.request.matchdict['culture'])
        if culture not in default_cultures:
            raise HTTPBadRequest("Incorrect culture")

        return id, culture

    def _get_document(self, id, culture):
        url = '%s/%s/%d?l=%s' % (
            self.settings['api_url'], self._API_ROUTE, id, culture
        )
        resp, document = self._call_api(url)
        # TODO: better error handling
        if resp['status'] == '404':
            raise HTTPNotFound()
        elif resp['status'] != '200':
            raise HTTPInternalServerError(
                "An error occured while loading the document")
        # We need to pass locale data to Mako as a dedicated object to make it
        # available to the parent templates:
        locale = document['locales'][0]
        return document, locale

    def _get_documents(self):
        url = '%s/%s' % (self.settings['api_url'], self._API_ROUTE)
        resp, content = self._call_api(url)
        # TODO: better error handling
        if resp['status'] == '200':
            return content['documents'], content['total']
        else:
            return [], 0

    def _get_geometry(self, data):
        return asShape(json.loads(data))

    def _transform(self, geometry, source_epsg, dest_epsg):
        source_proj = pyproj.Proj(init=source_epsg)
        dest_proj = pyproj.Proj(init=dest_epsg)
        project = partial(pyproj.transform, source_proj, dest_proj)
        return transform(project, geometry)
