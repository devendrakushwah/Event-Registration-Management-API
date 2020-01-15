# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class SignUpView(APIView):

    def post(self, request):
        username, password, email, first_name, last_name = None, None, None, None, None
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
        except:
            # print(username, password, email, first_name, last_name)
            content = {'error': 'missing parameters'}
            return Response(content)
        try:
            if username and password and email and first_name and last_name:
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                content = {'user': 'success'}
                return Response(content)
            else:
                content = {'error': 'missing parameters'}
                return Response(content)
        except:
            return Response({'error': 'username already in use'})


class MyInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        content = {'id': user.id,
                   'username': user.username,
                   'email': user.email,
                   'first_name': user.first_name,
                   'last_name': user.last_name}
        return Response(content)
