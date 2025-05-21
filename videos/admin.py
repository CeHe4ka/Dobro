from django.contrib import admin
from .models import Video, ViewLog
from .models import Favorite
# Register your models here.
admin.site.register(Video)
admin.site.register(ViewLog)
admin.site.register(Favorite)