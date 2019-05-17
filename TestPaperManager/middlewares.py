from django.utils.deprecation import MiddlewareMixin


class Cros(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = 'OPTIONS, GET, PUT, POST, DELETE'
        response['Access-Control-Allow-Headers'] = 'content-type,xfilecategory,xfilename,xfilesize'
        response['Access-Control-Allow-Credentials'] = True
        return response
