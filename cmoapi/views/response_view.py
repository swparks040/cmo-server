from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import Response, Message, CMOUser
from datetime import date

class ResponseView(ViewSet):

    def retrieve(self, request, pk):
        try: 
            response = Response.objects.get(pk=pk)
        except Response.DoesNotExist:
            return Response({"message": "Response does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = ResponseSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        responses = Response.objects.all().order_by('created_on')
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):  
        message = Message.objects.get(pk=request.data['message'])
        author = CMOUser.objects.get(user=request.auth.user)
        response = Response.objects.create(
            message=message,
            author=author,
            content=request.data["content"],
            created_on=date.today()
            )
        serializer = ResponseSerializer(response)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        response = Response.objects.get(pk=pk)
        response.message = Message.objects.get(pk=request.data['message'])
        response.author = CMOUser.objects.get(user=request.auth.user)
        response.content = request.data["content"]
        response.created_on = date.today()
        response.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        response = Response.objects.get(pk=pk)
        response.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CMOUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMOUser
        fields = ('username', 'tokenNumber',  )
class ResponseSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Response
            fields = ('id', 'message', 'author', 'content', 'created_on', )