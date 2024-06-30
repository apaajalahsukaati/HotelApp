import sys
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def get_default_status():
    first_status = StatusModel.objects.first()
    if first_status:
        return first_status.pk
    else:
        return None

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username) + ' ' + str(self.first_name) + ' ' + str(self.last_name)


class StatusModel(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif')
    )
    name = models.CharField(max_length=50, unique=True)
    status = models.TextField(blank=True, null=True)
    user_create = models.ForeignKey(User, related_name='user_create_status_model', blank=True, null=True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(User, related_name='user_update_status_model', blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.PROTECT)
    avatar = models.ImageField(default=None, upload_to='profile_images/', blank=True, null=True)
    biografi = models.TextField()
    status = models.ForeignKey(StatusModel, related_name='status_profile', default=None, on_delete=models.PROTECT)
    user_create = models.ForeignKey(User, related_name='user_create_profile', blank=True, null=True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(User, related_name='user_update_profile', blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.id}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        if self.id:
            try:
                this = Profile.objects.get(id=self.id)
                if this.avatar and this.avatar != self.avatar:
                    this.avatar.delete(save=False)
            except Profile.DoesNotExist:
                pass

        if self.avatar:
            var_avatar = self.avatar
            self.avatar = compress_image(var_avatar, 'profile')

        super(Profile, self).save(*args, **kwargs)


def compress_image(image, category):
    img = Image.open(image)
    img = img.convert('RGB')
    output = BytesIO()
    img.save(output, format='JPEG', quality=85)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}_{category}.jpg", 'image/jpeg', sys.getsizeof(output), None)

class KategoriPulau(models.Model):
    pulau = models.CharField(max_length = 100)
    status = models.ForeignKey(StatusModel, related_name= 'status_pulau', default=get_default_status, on_delete=models.PROTECT)

    def __str__(self):
        return self.pulau


class TableListHotel(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif')
    )
    # status_table_choices = (
    #     ('Buka', 'Buka'),
    #     ('Tutup', 'Tutup'),
    # )

    code = models.CharField(max_length=100)
    name = models.TextField(max_length=100)
    # table_status = models.CharField(max_length=15, choices=status_table_choices, default='Buka' )
    status = models.CharField(max_length=15, choices=status_choices, default='Aktif')
    user_create = models.ForeignKey(User, related_name='user_create_table_listhotel', blank=True, null=True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(User, related_name='user_update_table_listhotel', blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RatingBintang(models.Model):
    jumlah_bintang_hotel_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    nama = models.CharField(max_length=3, null=False, blank= False ,default= None)
    jumlah_bintang_hotel = models.CharField(max_length=100, choices=jumlah_bintang_hotel_choices, default='1')

    def __str__(self):
        return self.nama


class DetailHotel(models.Model):
    hotel = models.ForeignKey(TableListHotel, on_delete=models.CASCADE, related_name='detail')
    pulau = models.ForeignKey(KategoriPulau, on_delete=models.CASCADE, related_name='detail', default= KategoriPulau.objects.first().pk)
    alamat = models.TextField(max_length=100)
    deskripsi = models.TextField()
    fasilitas = models.TextField()
    informasi_kamar = models.TextField()
    google_maps_link = models.URLField(max_length=100, blank=True, null=True)
    rating_bintang = models.ForeignKey(RatingBintang, related_name='rating_detail_hotel', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"DetailHotel {self.hotel.name}"

