from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from api.models import Category, Content, ApiUser


class ApiUserInline(admin.StackedInline):
    model = ApiUser
    can_delete = False
    verbose_name_plural = 'ApiUser'
    fk_name = 'user'


admin.site.unregister(User)


@admin.register(User)
class ApiUserAdmin(UserAdmin):
    inlines = (ApiUserInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_premium')
    list_select_related = ('apiuser',)

    def get_premium(self, instance):
        return instance.apiuser.is_premium

    get_premium.short_description = 'Premium'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(ApiUserAdmin, self).get_inline_instances(request, obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):

    list_display = ('title', 'categories', 'is_premium')

    def categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    