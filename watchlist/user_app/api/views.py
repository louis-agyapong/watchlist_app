from http import HTTPStatus

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer


@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["response"] = "User registered successfully"
            data["username"] = user.username
            data["email"] = user.email

            # token = Token.objects.get(user=user).key
            # data["token"] = token
            refresh = RefreshToken.for_user(user)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        # else:
        #     data = serializer.errors
        # return Response(data)
            return Response(data, status=HTTPStatus.CREATED)
        return Response(data=serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(["POST"])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=HTTPStatus.OK)
