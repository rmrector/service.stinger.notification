import collections
import sys
import xbmc

if sys.version_info < (2, 7):
    import simplejson as json
else:
    import json

movie_properties = ['imdbnumber', 'tag']

nostingertags_filter = {'and': [{'field': 'tag', 'operator':'isnot', 'value':'duringcreditsstinger'}, {'field': 'tag', 'operator':'isnot', 'value':'aftercreditsstinger'}]}

def get_movies(sort_method='sorttitle', ascending=True, limit=None, properties=None, listfilter=None):
    json_request = get_base_json_request('VideoLibrary.GetMovies')
    json_request['params']['properties'] = properties if properties else movie_properties
    json_request['params']['sort'] = {'method': sort_method, 'order': 'ascending' if ascending else 'descending'}
    if listfilter:
        json_request['params']['filter'] = listfilter
    if limit:
        json_request['params']['limits'] = {'end': limit}

    json_result = execute_jsonrpc(json_request)
    if _check_json_result(json_result, 'movies', json_request):
        return json_result['result']['movies']
    else:
        return []

def set_movie_details(movie_id, **movie_details):
    json_request = get_base_json_request('VideoLibrary.SetMovieDetails')
    json_request['params']['movieid'] = movie_id
    for param, value in movie_details.iteritems():
        json_request['params'][param] = value

    json_result = execute_jsonrpc(json_request)
    _check_json_result(json_result, 'OK', json_request)

def get_base_json_request(method):
    return {'jsonrpc': '2.0', 'method': method, 'params': {}, 'id': 1}

def execute_jsonrpc(jsonrpc_command):
    if isinstance(jsonrpc_command, dict):
        jsonrpc_command = json.dumps(jsonrpc_command, ensure_ascii=False)
        if isinstance(jsonrpc_command, unicode):
            jsonrpc_command = jsonrpc_command.encode('utf-8')

    json_result = xbmc.executeJSONRPC(jsonrpc_command)
    return _json_unicode_to_str(json.loads(json_result))

def _json_unicode_to_str(jsoninput):
    """Converts values in a data object from JSON to utf-8."""
    if isinstance(jsoninput, dict):
        return {key: _json_unicode_to_str(value) for key, value in jsoninput.iteritems()}
    elif isinstance(jsoninput, list):
        return [_json_unicode_to_str(item) for item in jsoninput]
    elif isinstance(jsoninput, unicode):
        return jsoninput.encode('utf-8')
    else:
        return jsoninput

def _check_json_result(json_result, result_key, json_request):
    if 'error' in json_result:
        raise JsonException(json_request, json_result)

    return 'result' in json_result and result_key in json_result['result']

class JsonException(Exception):
    def __init__(self, json_request, json_result):
        self.json_request = json_request
        self.json_result = json_result

        message = "There was an error with a JSON-RPC request.\nRequest: "
        message += json.dumps(json_request, skipkeys=True, ensure_ascii=False, indent=2, cls=LogJSONEncoder)
        message += "\nResult: "
        message += json.dumps(json_result, skipkeys=True, ensure_ascii=False, indent=2, cls=LogJSONEncoder)

        if isinstance(message, unicode):
            message = message.encode('utf-8')
        super(JsonException, self).__init__(message)

class LogJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, collections.Mapping):
            return dict((key, obj[key]) for key in obj.keys())
        if isinstance(obj, collections.Iterable):
            return list(obj)
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)
