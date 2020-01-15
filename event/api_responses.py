from rest_framework import status
from rest_framework.response import Response


class ApiResponse:
    """Include Functions to send error msgs in proper format"""

    @staticmethod
    def bad(contents, status_code):
        response = dict()
        response['error'] = contents
        response['error_type'] = 'GENERIC'
        return Response(response, status=status_code)

    @staticmethod
    def good(contents, status_code):
        response = dict()
        response['success'] = True
        response['message'] = contents
        return Response(response, status=status_code)

    @staticmethod
    def forbidden(contents='Access Denied'):
        return ApiResponse.bad(contents, status.HTTP_403_FORBIDDEN)

    @staticmethod
    def unauthorized(contents):
        return ApiResponse.bad(contents, status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def success(contents):
        return ApiResponse.good(contents, status.HTTP_200_OK)

    @staticmethod
    def bad_request(contents):
        return ApiResponse.bad(contents, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def no_content():
        return Response(status=status.HTTP_204_NO_CONTENT)
