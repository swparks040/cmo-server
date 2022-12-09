from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import PTO

class PTOView(ViewSet):
    """CMO PTO view"""

    def retrieve(self, request, pk):
        try: 
            pto = PTO.objects.get(pk=pk)
        except PTO.DoesNotExist:
            return Response({"message": "PTO does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = PTOSerializer(pto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        ptos = PTO.objects.all().order_by('user')
        serializer = PTOSerializer(ptos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        pto = PTO.objects.create(
            cmouser=request.data["cmouser"],
            total_days=request.data["total_days"],
            days_used=request.data["days_used"],
            days_remaining=request.data["days_remaining"]
            )
        serializer = PTOSerializer(pto)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        pto = PTO.objects.get(pk=pk)
        pto.cmouser = request.data["cmouser"]
        pto.total_days = request.data["total_days"]
        pto.days_used = request.data["days_used"]
        pto.days_remaining = request.data["days_remaining"]
        pto.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        pto = PTO.objects.get(pk=pk)
        pto.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PTOSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PTO
        fields = ('id', 'cmouser', 'total_days', 'days_used', 'days_remaining', )