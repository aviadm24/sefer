from django.contrib import admin
from .models import Index, Texts, MainCategories


class IndexAdmin(admin.ModelAdmin):
    pass


class TextsAdmin(admin.ModelAdmin):
    pass


class MainCategoriesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Index, IndexAdmin)
admin.site.register(Texts, TextsAdmin)
admin.site.register(MainCategories, MainCategoriesAdmin)
