from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from cmoapi.models import CMOUser


class CMOUserView(ViewSet):

    def retrieve(self, request, pk):
        if (pk=="current"):
            user=request.auth.user
            cmouser=CMOUser.objects.get(user=user)
            data={
                "id": cmouser.id,
                "is_staff": user.is_staff,
            }
            return Response(data, status=status.HTTP_200_OK)
        try:
            cmouser = CMOUser.objects.get(pk=pk)
        except CMOUser.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CMOUserSerializer(cmouser)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        cmousers = CMOUser.objects.all()
        serializer = CMOUserSerializer(cmousers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        cmouser = CMOUser.objects.create(
            user=request.data["user"],
            full_name=request.data["full_name"],
            job_position=request.data["job_position"],
            salary=request.data["salary"],
            birthday=request.data["birthday"],
            date_hired=request.data["date_hired"],
            date_evaluated=request.data["date_evaluated"],
            date_promoted=request.data["date_promoted"],
            profile_image_url=request.data["profile_image_url"],
        )
        serializer = CMOUserSerializer(cmouser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        cmouser = CMOUser.objects.get(pk=pk)
        user = User.objects.get(pk=cmouser.user_id)
        user.is_staff = request.data["is_staff"]
        cmouser.full_name = request.data["full_name"]
        cmouser.job_position = request.data["job_position"]
        cmouser.salary = request.data["salary"]
        cmouser.birthday = request.data["birthday"]
        cmouser.date_hired = request.data["date_hired"]
        cmouser.date_evaluated = request.data["date_evaluated"]
        cmouser.date_promoted = request.data["date_promoted"]
        cmouser.profile_image_url = request.data["profile_image_url"]
        user.save()
        cmouser.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        cmouser = CMOUser.objects.get(pk=pk)
        cmouser.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined")

class CMOUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    class Meta:
        model = CMOUser
        fields = (
            "id",
            "user",
            "full_name",
            "job_position",
            "salary",
            "birthday",
            "date_hired",
            "date_evaluated",
            "date_promoted",
            "profile_image_url",
        )
