from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import Response

class ResponseView(ViewSet):

    def retrieve(self, request, pk):
        try: 
            response = Response.objects.get(pk=pk)
        except Response.DoesNotExist:
            return Response({"message": "Response does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = ResponseSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        responses = Response.objects.all().order_by('title')
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):      
        response = Response.objects.create(
            message=request.data["message"],
            author=request.data["author"],
            content=request.data["content"],
            created_on=request.data["created_on"]
            )
        serializer = ResponseSerializer(response)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        response = Response.objects.get(pk=pk)
        response.message = request.data["message"]
        response.author = request.data["author"]
        response.content = request.data["content"]
        response.created_on = request.data["created_on"]
        response.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        response = Response.objects.get(pk=pk)
        response.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ResponseSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Response
            fields = ('id', 'message', 'author', 'content', 'created_on', )