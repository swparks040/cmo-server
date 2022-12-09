from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import Message

class MessageView(ViewSet):
    """CMO messages view"""

    def retrieve(self, request, pk):
        try: 
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"message": "Message does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        messages = Message.objects.all().order_by('title')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def create(self, request):
        message = Message.objects.create(
            cmouser=request.data["cmouser"],
            category=request.data["category"],
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            content=request.data["content"]
            )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.cmouser = request.data["cmouser"]
        message.category = request.data["category"]
        message.title = request.data["title"]
        message.publication_date = request.data["publication_date"]
        message.content = request.data["content"]
        message.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class MessageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Message
        fields = ('id', 'cmouser', 'category', 'title', 'publication_date', 'content', )