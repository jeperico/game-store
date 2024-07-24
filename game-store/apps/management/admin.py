from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Games, Player, User, Genre, Category
# Register your models here.
class GamesAdmin(admin.ModelAdmin):
    list_display = ('title', 'parental_rating', 'price', 'release_date', 'category', 'updated_at')
    search_fields = ['title', 'category', 'parental_rating']

admin.site.register(Games, GamesAdmin)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']

admin.site.register(Genre, GenreAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday')
    search_fields = ['name']

admin.site.register(Player, PlayerAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active", "is_superuser"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def get_fieldsets(self, request, obj=None):
        if obj:
            return [(None, {"fields": ("name", "email", "is_active")})]
        return [
            (None, {"fields": ("name", "email", "password", "is_active")})
        ]

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)