from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Timer
from timer import serializers


class TimerListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=serializers.TimerDetailSerializer(many=True)
    )
    def get(self, request):
        timers = Timer.objects.filter(user=request.user).order_by('-id')
        serializer = serializers.TimerDetailSerializer(timers, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=serializers.TimerSerializer,
        responses=serializers.TimerSerializer
    )
    def post(self, request):
        serializer = serializers.TimerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimerDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Timer.objects.get(pk=pk, user=user)
        except Timer.DoesNotExist:
            return None

    @extend_schema(
        responses={
            200: serializers.TimerSerializer,
            404: OpenApiResponse(description="Not found.")
        }
    )
    def get(self, request, pk):
        timer = self.get_object(pk, request.user)
        if not timer:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.TimerSerializer(timer)
        return Response(serializer.data)

    @extend_schema(
        request=serializers.TimerSerializer,
        responses={
            200: serializers.TimerSerializer,
            400: OpenApiResponse(description="Validation error."),
            404: OpenApiResponse(description="Not found.")
        }
    )
    def put(self, request, pk):
        timer = self.get_object(pk, request.user)
        if not timer:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.TimerSerializer(timer, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Deleted successfully."),
            404: OpenApiResponse(description="Not found.")
        }
    )
    def delete(self, request, pk):
        timer = self.get_object(pk, request.user)
        if not timer:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        timer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
