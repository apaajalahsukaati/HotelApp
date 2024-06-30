from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from hotel_app.models import TableListHotel, DetailHotel, RatingBintang, KategoriPulau, StatusModel
from api.serializers import TableListHotelSerializers, DetailHotelSerializers, RatingBintangSerializers, KategoriPulauSerializer, RegisterUserSerializer, LoginSerializer
from django.contrib.auth import login as django_login 
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import logout
from .paginators import  CustomPagination
# from django_filters.rest_framework import DjangoFilterBackend



class TableListHotelViews(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        table_listhotel = TableListHotel.objects.filter(status='Aktif')
        serializer = TableListHotelSerializers(table_listhotel, many=True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Pembacaan seluruh data berhasil',
            'user' :str(request.user),
            'auth' :str(request.auth),
            'data' : serializer.data,
        }
        return Response(response, status= status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
        }
        serializer = TableListHotelSerializers(data=data)
        if serializer.is_valid():
            serializer.save()   
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Data Berhasil Dibuat....',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailHotelViews(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return DetailHotel.objects.get(id=id)
        except DetailHotel.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        if id:
            detail_hotel = self.get_object(id)
            if not detail_hotel:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Data tidak ada',
                        'data': {}
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            serializer = DetailHotelSerializers(detail_hotel)
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diambil',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            detail_hotels = DetailHotel.objects.all()
            serializer = DetailHotelSerializers(detail_hotels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id=None, *args, **kwargs):
        detail_hotel = self.get_object(id)
        if not detail_hotel:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Data tidak ada',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'hotel': request.data.get('hotel'),
            'alamat': request.data.get('alamat'),
            'deskripsi': request.data.get('deskripsi'),
            'fasilitas': request.data.get('fasilitas'),
            'gambar_hotel': request.data.get('gambar_hotel'),
            'informasi_kamar': request.data.get('informasi_kamar'),
            'google_maps_link': request.data.get('google_maps_link'),
            'rating_bintang': request.data.get('rating_bintang'),
        }
        serializer = DetailHotelSerializers(instance=detail_hotel, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diupdate',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id=None, *args, **kwargs):
        detail_hotel = self.get_object(id)
        if not detail_hotel:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Data tidak ada',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        detail_hotel.delete()
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data berhasil dihapus'
        }
        return Response(response, status=status.HTTP_200_OK)



class RatingBintangViews(APIView):
    def get(self, request, *args, **kwargs):
        rating_bintang = RatingBintang.objects.all()
        serializer = RatingBintangSerializers(rating_bintang, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'hotel': request.data.get('hotel'),
            'jumlah_bintang_hotel': request.data.get('jumlah_bintang_hotel'),
            'ulasan': request.data.get('ulasan')
        }
        serializer = RatingBintangSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Rating Bintang Berhasil Dibuat....',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KategoriPulauViews(APIView):
    def get(self, request, *args, **kwargs):
        kategori_pulau = KategoriPulau.objects.all()
        serializer = KategoriPulauSerializer(kategori_pulau, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'pulau': request.data.get('pulau'),
        }
        serializer = KategoriPulauSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Data created successfully...',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterUserAPIView(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Selamat anda telah terdaftar...',
                'data' : serializer.data,
            }
            return Response(response_data, status = status.HTTP_201_CREATED)
        return Response({
                'status' : status.HTTP_400_BAD_REQUEST,
                'data' : serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
    
class LoginView(GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        
        # Membuat atau mengambil token autentikasi
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Selamat anda berhasil masuk...',
            'data': {
                'token': token.key,  # Mengirim token autentikasi
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin,
                'is_user': user.is_user,
            }
        })
    
class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Logout berhasil'
        }
        return Response(response, status=status.HTTP_200_OK)
    
class TableListHotelFilterApi(generics.ListAPIView):
    queryset = TableListHotel.objects.all()
    serializer_class = TableListHotelSerializers
    pagination_class = CustomPagination
    permissions_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend,]
    ordering_fields = ['created_on']