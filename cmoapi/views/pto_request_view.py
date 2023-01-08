from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cmoapi.models import PTO, CMOUser, PTORequest

class PTORequestView(ViewSet):
    """CMO PTO requests view"""

    def retrieve(self, request, pk):
        try:
            pto_request = PTORequest.objects.get(pk=pk)
        except PTORequest.DoesNotExist:
            return Response({"message": "PTO request does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = PTORequestSerializer(pto_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        pto_requests = PTORequest.objects.all()

        if "cmouser" in request.query_params:
            query_value = request.query_params["cmouser"]
            pto_requests = pto_requests.filter(cmouser=query_value)

        filter_by = request.query_params.get('user', None)
        if filter_by is not None:
            pto_requests = pto_requests.filter(cmouser__user=request.auth.user)
        serializer = PTORequestSerializer(pto_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        cmouser = CMOUser.objects.get(user=request.auth.user)
        pto = PTO.objects.get(pk=request.data["pto"])
        pto_request = PTORequest.objects.create(
            cmouser=cmouser,
            pto=pto,
            start_date=request.data["start_date"],
            end_date=request.data["end_date"],
            days_requested=request.data["days_requested"],
            justification=request.data["justification"],
            is_approved=False,
        )
        serializer = PTORequestSerializer(pto_request)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        cmouser = CMOUser.objects.get(user=request.auth.user)
        pto_request = PTORequest.objects.get(pk=pk)
        pto = PTO.objects.get(pk=pk)
        cmouser = cmouser
        pto = pto
        pto_request.start_date = request.data["start_date"]
        pto_request.end_date = request.data["end_date"]
        pto_request.days_requested = request.data["days_requested"]
        pto_request.justification = request.data["justification"]
        pto_request.is_approved = request.data["is_approved"]
        cmouser.save()
        pto_request.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        pto_request = PTORequest.objects.get(pk=pk)
        pto_request.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PTORequestSerializer(serializers.ModelSerializer):
    """JSON serializer for PTO requests"""
    class Meta:
        model = PTORequest
        fields = ('id', 'cmouser', 'pto', 'start_date', 'end_date', 'days_requested', 'justification', 'is_approved', )
        depth = 1

