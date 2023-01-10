from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import Message, CMOUser, Category
from datetime import date


class MessageView(ViewSet):
    """CMO messages view"""

    def retrieve(self, request, pk):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"message": "Message does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        messages = Message.objects.all().order_by('title')
        filter_by = request.query_params.get('user', None)
        if filter_by is not None:
            messages = messages.filter(cmouser__user=request.auth.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        cmouser = CMOUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        message = Message.objects.create(
            cmouser=cmouser,
            category=category,
            title=request.data["title"],
            publication_date=date.today(),
            content=request.data["content"],
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.title = request.data["title"]
        message.content = request.data["content"]
        category = Category.objects.get(pk=request.data["category"])
        message.category = category
        message.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'cmouser', 'category', 'title',
                  'publication_date', 'content', )
        depth = 2
