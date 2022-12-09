from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import FamilyMemberRelationship

class FamilyMemberRelationshipView(ViewSet):

    def retrieve(self, request, pk):
        try: 
            family_member_relationship = FamilyMemberRelationship.objects.get(pk=pk)
        except FamilyMemberRelationship.DoesNotExist:
            return Response({"message": "Family member relationship does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = FamilyMemberRelationshipSerializer(family_member_relationship)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        family_member_relationships = FamilyMemberRelationship.objects.all().order_by('label')
        serializer = FamilyMemberRelationshipSerializer(family_member_relationships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        family_member_relationship = FamilyMemberRelationship.objects.create(
            label=request.data["label"],
            )
        serializer = FamilyMemberRelationshipSerializer(family_member_relationship)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        family_member_relationship = FamilyMemberRelationship.objects.get(pk=pk)
        family_member_relationship.label = request.data["label"]
        family_member_relationship.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        family_member_relationship = FamilyMemberRelationship.objects.get(pk=pk)
        family_member_relationship.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class FamilyMemberRelationshipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FamilyMemberRelationship
        fields = ('id', 'label', )