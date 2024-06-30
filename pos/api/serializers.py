from rest_framework import serializers
from hotel_app.models import (
    User,StatusModel,Profile,TableListHotel,DetailHotel,RatingBintang,KategoriPulau
)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_admin', 'is_user', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password1': 'Kata sandi dan Ulang kata sandi tidak sama...'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Hapus password2 dari data yang akan disimpan
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_admin=validated_data['is_admin'],
            is_user=validated_data['is_user'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer) :
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
    
        if username and password:
            user = authenticate(username = username, password = password) 
            if user :   
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    data['user'] = user 
                    data['token'] = token.key
                else:
                    msg = ' Status pengguna tidak aktif...'
                    raise ValidationError({'message' : msg})
            else :
                msg = 'Anda tidak memiliki akses masuk'
                raise ValidationError({'message' : msg})
        else:
            msg = 'Mohon mengisi kolom nama pengguna dan kata sandi'
            raise ValidationError({'message' : msg})
        return data
    

class RatingBintangSerializers(serializers.ModelSerializer):
    hotel = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = RatingBintang
        fields = ('id','hotel','jumlah_bintang_hotel')

class TableListHotelSerializers(serializers.ModelSerializer):
    rating_bintang = RatingBintangSerializers(many=True, read_only=True, source='rating_list_hotel')
    
    class Meta:
        model = TableListHotel
        fields = ('id', 'code', 'name', 'status', 'rating_bintang')

class DetailHotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = DetailHotel
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['rating_bintang'] = instance.rating_bintang.jumlah_bintang_hotel if instance.rating_bintang else None
        return response
        
class KategoriPulauSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name', read_only=True)
    
    class Meta:
        model = KategoriPulau
        fields = ('id', 'pulau', 'status')
        
        