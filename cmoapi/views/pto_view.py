from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import PTO, CMOUser


class PTOView(ViewSet):
    """CMO PTO view"""

    def retrieve(self, request, pk):
        try:
            pto = PTO.objects.get(pk=pk)  
        except PTO.DoesNotExist:
            return Response({"message": "PTO does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PTOSerializer(pto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        ptos = PTO.objects.all()

        if "cmouser" in request.query_params:
            query_value = request.query_params["cmouser"]
            ptos = ptos.filter(cmouser=query_value)
            
        filter_by = request.query_params.get('user', None)
        if filter_by is not None:
            ptos = ptos.filter(cmouser__user=request.auth.user)
        serializer = PTOSerializer(ptos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        cmouser = CMOUser.objects.get(user=request.auth.user)
        pto = PTO.objects.create(
            cmouser=cmouser,
            total_days=request.data["total_days"],
            days_used=request.data["days_used"],
            days_remaining=request.data["days_remaining"]
        )
        serializer = PTOSerializer(pto)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        fields = ('id', 'cmouser', 'total_days',
                  'days_used', 'days_remaining', )
