from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from cmoapi.models import CMOUser


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    """

    username = request.data["username"]
    password = request.data["password"]

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)

        data = {
            "valid": True,
            "token": token.key,
            "is_staff": authenticated_user.is_staff
        }
        return Response(data)

    else:
        data = {"valid": False}
        return Response(data)

@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new CMOUser for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email'],
        is_staff=request.data['is_staff']
    )

    # Now save the extra info in the cmoapi_CMOUser table
    cmouser = CMOUser.objects.create(
        user=new_user,
        job_position=request.data['job_position'],
        salary=request.data['salary'],
        birthday=request.data['birthday'],
        date_hired=request.data['date_hired'],
        date_evaluated=request.data['date_evaluated'],
        date_promoted=request.data['date_promoted'],
        profile_image_url=request.data['profile_image_url']
    )
    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=cmouser.user)
    # Return the token to the client
    data = { 'token': token.key }
    return Response(data)