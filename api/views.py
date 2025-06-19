from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import TaskSerializers, CalendarTasktSerializers, UserSerializer
from .models import TaskModel, CalendarTaskModel
from django.conf import settings
from django.contrib.auth import get_user_model


class BaseTaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    model = None
    serializer_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        queryset = self.model.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(BaseTaskViewSet):
    model = TaskModel
    serializer_class = TaskSerializers


class CalendarTaskViewSet(BaseTaskViewSet):
    model = CalendarTaskModel
    serializer_class = CalendarTasktSerializers


class ContactViewSet(viewsets.ViewSet):
    def create(self, request):
        name = request.data.get("name")
        message = request.data.get("message")
        email = request.data.get("email")

        subject = f'contact from {name}'
        full_message = f'\nmailaddress: {email}\n\nsentence: \n{message}'

        if not (name and message and email):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            subject, full_message, settings.DEFAULT_FROM_EMAIL, ["h.hatori0603@gmail.com"], fail_silently=False,
        )

        return Response({"message": "send mail successful!!"}, status=status.HTTP_200_OK)


class UserSingnupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserExistsView(APIView):
    def get(self, request):
        User = get_user_model()
        username = request.query_params.get('username')
        email = request.query_params.get('email')

        exist = User.objects.filter(username=username, email=email).exists()

        return Response(exist, status=status.HTTP_200_OK)
