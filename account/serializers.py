from django.contrib.auth import authenticate
from rest_framework import serializers

from account.models import MyUser
from account.tasks import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,write_only=True)
    password_confirm = serializers.CharField(min_length=6,write_only=True)
    class Meta:
        model = MyUser
        fields = ['email','password','password_confirm']

    def validate(self,validated_data):
        #{'password':'helloworld',"password_confirm":"helloworld","email":"test@test.com"}
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('password do not match')
        return validated_data

    def create(self, validated_data):
        """this function it`s cool """
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects._create_user(email=email,password=password)
        send_activation_code.delay(email=user.email,activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='password',
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email,password=password)
            if not user:
                message = 'anable to lock in with provided credenstions'
                return serializers.ValidationError(message,code='authorization')
        else:
            message = 'must include "email" and "password".'
            raise serializers.ValidationError(message,code='authorization')
        attrs['user'] = user
        return attrs



class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    activation_code = serializers.CharField(max_length=6,min_length=6,required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6,required=True)

    def validate_email(self,email):
        if not MyUser.objects.filter(email=email,is_active=False).exists():
            raise serializers.ValidationError('Пользователь с таким emailom не найден!*1!')
        return email

    def validate_activation_code(self,activation_code):
        if not MyUser.objects.filter(activation_code=activation_code, is_active=False).exists():
            raise serializers.ValidationError('Пользователь с таким активационным кодом не найден!*1!')
        return activation_code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self,**kwargs):
        data = self.validated_data
        email = data.get('email')
        code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.get(email=email,activation_code=code,is_active=False)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user

