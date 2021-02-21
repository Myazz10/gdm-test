from django.contrib import admin
from .models import Photo, Video, Audio, ErrorCharacter

# Register your models here.
admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(ErrorCharacter)