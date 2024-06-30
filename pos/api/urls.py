from django.urls import path,include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import(
    TableListHotelViews,DetailHotelViews,RegisterUserAPIView,LoginView,LogoutView, TableListHotelFilterApi, TableListHotelFilterApi
)

app_name = 'api'
urlpatterns = [

    path('api/register', RegisterUserAPIView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/logout', LogoutView.as_view()),
    path('api/table_list_hotel_filter', TableListHotelFilterApi.as_view()),
    path('api/table_listhotel',views.TableListHotelViews.as_view()),
    path('api/detailhotel', views.DetailHotelViews.as_view(), name='detailhotel'),
    path('api/detailhotel/<int:id>', views.DetailHotelViews.as_view(), name='detailhotel_detail'),
    path('api/rating_bintang', views.RatingBintangViews.as_view()),
    path('api/kategori_pulau', views.KategoriPulauViews.as_view()),
    path('api/table-list-hotel-filter/', views.TableListHotelFilterApi.as_view())

]