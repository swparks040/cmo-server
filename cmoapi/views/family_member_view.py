from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import FamilyMember, CMOUser, FamilyMemberRelationship

class FamilyMemberView(ViewSet):
    """CMO family members view"""

    def retrieve(self, request, pk):
        try: 
            family_member = FamilyMember.objects.get(pk=pk)
        except FamilyMember.DoesNotExist:
            return Response({"message": "Family member does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = FamilyMemberSerializer(family_member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        family_members = FamilyMember.objects.all()

        if "cmouser" in request.query_params:
            query_value = request.query_params["cmouser"]
            family_members = family_members.filter(cmouser=query_value)
            
        filter_by = request.query_params.get('user', None)
        if filter_by is not None:
            family_members = family_members.filter(cmouser__user=request.auth.user)
        serializer = FamilyMemberSerializer(family_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        cmouser = CMOUser.objects.get(user=request.auth.user)
        family_member_relationship = FamilyMemberRelationship.objects.get(pk=request.data["family_member_relationship"])
        family_member = FamilyMember.objects.create(
            cmouser=cmouser,
            family_member_relationship=family_member_relationship,
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            birthday=request.data["birthday"],
            anniversary=request.data["anniversary"],
            graduation=request.data["graduation"]
            )
        serializer = FamilyMemberSerializer(family_member)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        cmouser = CMOUser.objects.get(user=request.auth.user)
        family_member = FamilyMember.objects.get(pk=pk)
        family_member_relationship = FamilyMemberRelationship.objects.get(pk=request.data["family_member_relationship"])
        cmouser = cmouser
        family_member_relationship = family_member_relationship
        family_member.first_name = request.data["first_name"]
        family_member.last_name = request.data["last_name"]
        family_member.birthday = request.data["birthday"]
        family_member.anniversary = request.data["anniversary"]
        family_member.graduation = request.data["graduation"]
        cmouser.save()
        family_member.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        family_member = FamilyMember.objects.get(pk=pk)
        family_member.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class FamilyMemberSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = FamilyMember
        fields = ('id', 'cmouser', 'family_member_relationship', 'first_name', 'last_name', 'birthday', 'anniversary', 'graduation', )