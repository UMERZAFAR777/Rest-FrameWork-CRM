from django.shortcuts import render
from account.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer,ChangePasswordSerializer,ResetMail,ResetPasswordSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }






class RegisterForm(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            token = get_tokens_for_user(data)
            return Response({'token': token, 'serializer_data': serializer.data}, status=status.HTTP_200_OK)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginForm(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email = email,password = password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response ({'token':token,'message':'Login Successfully........!'},status=status.HTTP_200_OK)
            else:
                return Response ({'message':'There was a error plz try again...!'},status=status.HTTP_400_BAD_REQUEST)

        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)    


class ProfileForm(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = ProfileSerializer(request.user)
      
        return Response( serializer.data, status=status.HTTP_200_OK)
       



class ChangePasswordForm(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = ChangePasswordSerializer(data = request.data,context={'user':request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password Change Successfully.....!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class ResetMailForm(APIView):
    def post(self,request):
        serializer = ResetMail(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Email sent check inbox....!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# class ResetPasswordForm(APIView):
#     def post(self, request, uid, token):
#         serializer = ResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'message': 'Password has been reset successfully!'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import logging
logger = logging.getLogger(__name__)

class ResetPasswordForm(APIView):
    def post(self, request, uid, token):
        logger.info(f"Request received with UID: {uid}, Token: {token}")
        serializer = ResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



      

