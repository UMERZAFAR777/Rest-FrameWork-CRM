from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import *


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['id','name','email','tc','password','password2']
        extra_kwargs = {
            'password':{
            'write_only' : True
            }
        }


    def validate(self, attrs):
        password = attrs.get('password')    
        password2 = attrs.get('password2')    

        if password != password2:
            raise serializers.ValidationError("Both Password doesnt match....!")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        model = User
        fields = ['email','password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email']




class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input':'password'},write_only = True)
    password2 = serializers.CharField(style={'input':'password2'},write_only= True)

    class Meta:
        fields = ['password','password2']


    def validate(self, attrs):
        password = attrs.get('password')    
        password2 = attrs.get('password2')

        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError('Both password doesnt match.....!')
        
        user.set_password(password)
        user.save()
        return attrs
    


class ResetMail(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        


        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)    

            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('user id =',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('user token =',token)
            link = 'http://www.localhost:3000/account/reset/'+uid+'/'+token
            print(link)
            body = 'Click Reset following password'+link
            data = {
                'subject':'Reset your password',
                'body':body,
                'to_email':user.email

            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You r not register...!')


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check if passwords match
        if password != password2:
            raise serializers.ValidationError("Passwords do not match!")

        uid = self.context.get('uid')
        token = self.context.get('token')

        try:
            # Decode the user ID from uid
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            # Validate token using the user object and the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The token is invalid or expired!")

            # Set the new password for the user
            user.set_password(password)
            user.save()

            return attrs

        except User.DoesNotExist:
            raise serializers.ValidationError("User not found!")
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError("Invalid UID or token!")


