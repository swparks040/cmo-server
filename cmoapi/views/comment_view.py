from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import Comment, Message, CMOUser
from datetime import date

class CommentView(ViewSet):

    def retrieve(self, request, pk):
        try: 
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({"message": "Comment does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        comments = Comment.objects.all().order_by('created_on')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):  
        message = Message.objects.get(pk=request.data['message'])
        author = CMOUser.objects.get(user=request.auth.user)
        comment = Comment.objects.create(
            message=message,
            author=author,
            content=request.data["content"],
            created_on=date.today()
            )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.message = Message.objects.get(pk=request.data['message'])
        comment.author = CMOUser.objects.get(user=request.auth.user)
        comment.content = request.data["content"]
        comment.created_on = date.today()
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CMOUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMOUser
        fields = ('username', 'tokenNumber',  )
class CommentSerializer(serializers.ModelSerializer): 
        class Meta:
            model = Comment
            fields = ('id', 'message', 'author', 'content', 'created_on', )