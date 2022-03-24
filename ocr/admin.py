from django.contrib import admin
from .models import TaharaImage, Answers, Light, CameraDevice, CameraConfig, Comment
import base64
from django.utils.html import format_html


class TaharaImageAdmin(admin.ModelAdmin):
    readonly_fields = ["image_logo", ]

    def image_logo(self, obj):
        # print("utf: ", str(obj.logo)[2:-1])
        return format_html('<img src="data:image/png;base64,{}">', str(obj.logo)[2:-1])


admin.site.register(TaharaImage, TaharaImageAdmin)
admin.site.register(Answers)
admin.site.register(Light)
admin.site.register(CameraDevice)
admin.site.register(CameraConfig)
admin.site.register(Comment)
