from rest_framework.exceptions import APIException


class ImdbConnectionFailError(APIException):
    status_code = 503
    default_detail = 'Service Unavailable'
    default_code = 'ServiceUnavailable'
