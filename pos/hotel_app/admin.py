from django.contrib import admin
from hotel_app.models import User,StatusModel,Profile, TableListHotel,DetailHotel,RatingBintang,KategoriPulau

admin.site.register(User)
admin.site.register(StatusModel)
admin.site.register(Profile)
admin.site.register(TableListHotel)
admin.site.register(DetailHotel)
admin.site.register(RatingBintang)
admin.site.register(KategoriPulau)
