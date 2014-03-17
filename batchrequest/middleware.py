from urlparse import urlparse
import simplejson as json


class BatchResquestMiddleware(object):
    def __init__(self, application, endpoint=None):
        self.app = application
        self.endpoint = endpoint

    def __call__(self, environ, start_response, exc_info=None):

        if environ['PATH_INFO'] == self.endpoint:
            return self.batch_response(environ, start_response)

        return self.app(environ, start_response)

    def batch_response(self, environ, start_response):
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size) or '{}'

        # TODO: json decode error handling
        payload = json.loads(request_body)

        requests = payload.get('batch', [])
        result = []
        for request in requests:
            result.append(self.call_once(request, environ, start_response))

        response_body = json.dumps(result)

        start_response('200 OK', [
            ('Content-Length', len(response_body)),
            ('Content-Type', 'application/json'),
        ])
        return response_body

    def call_once(self, request, environ, start_response):
        def local_start(stat_str, headers=[]):
            local_start.status_code = int(stat_str.split(' ')[0])
            local_start.headers = headers
            return start_response(stat_str, headers)

        env = environ.copy()
        url = '{0}://{1}{2}'.format(env.get('wsgi.url_scheme', 'http'),
                                    env.get('HTTP_HOST', ''),
                                    request['path'])
        parsed = urlparse(url)
        env['REQUEST_METHOD'] = request.get('method', 'GET')
        env['PATH_INFO'] = parsed.path
        env['QUERY_STRING'] = parsed.query

        response = self.app(env, local_start)

        headers = []
        for t in sorted(local_start.headers):
            header = dict(name=t[0], value=t[1])
            headers.append(header)

        return dict(
                code=local_start.status_code,
                headers=headers,
                body=response,
                )

