from rest_framework import status,permissions
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from questions.models import Question
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .task import user_created

class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_created.delay(user.id)
            return Response({
                'data':serializer.data,
                'ok':'user created'

            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

