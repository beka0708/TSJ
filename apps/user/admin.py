from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.urls import path
from .models import PasswordReset
from .models import DeviceToken

CustomUser = get_user_model()

admin.site.register(PasswordReset)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "phone_number",
        "name",
        "email",
        "is_staff",
        "role",
        "is_active",
        "is_approved",
        "is_status",
        "verification_code"
    )
    ordering = ("name",)
    list_filter = ("is_status", "is_active")
    fieldsets = (
        (None, {"fields": ("name", "email", "address", "phone_number", "password")}),
        ("Доступы", {"fields": ("is_staff", "groups", "user_permissions")}),
        (
            "Одобрение",
            {
                "fields": (
                    "role",
                    "is_status",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "phone_number",
                    "email",
                    "address",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )
    search_fields = ("name", "email", "phone_number")

    def get_urls(self):
        urls = super(CustomUserAdmin, self).get_urls()
        custom_urls = [
            path(
                "get_user/<int:object_id>/",
                self.admin_site.admin_view(self.get_user),
                name="get_user",
            ),
        ]
        return custom_urls + urls

    def get_user(self, request, object_id):
        # try:
        user = CustomUser.objects.get(pk=object_id)
        if user.is_status != CustomUser.APPROVED:
            user.is_status = CustomUser.APPROVED
            user.is_active = True
            user.save()
        return redirect("admin:apps_user_changelist")

        # Получение token устройства пользователя
        #         device_token = DeviceToken.objects.filter(user=user).first()
        #         if device_token:
        #             # Отправка уведомления
        #             title = "Ваш аккаунт одобрен"
        #             body = "Вы можете войти в систему"
        #             send_notification(device_token.token, title, body)
        #         else:
        #             messages.warning(request, "Не удалось отправить уведомление: токен устройства не найден.")
        #     else:
        #         messages.info(request, f"Пользователь {user.name} уже одобрен.")
        # except CustomUser.DoesNotExist:
        #     messages.error(request, "Пользователь не найден.")
        # except Exception as e:
        #     messages.error(request, f"Произошла ошибка: {e}")
        # return redirect('admin:apps_user_changelist')


# class DeviceTokenAdmin(admin.ModelAdmin):
#     list_display = ("user", "token")
#
#
# admin.site.register(DeviceToken, DeviceTokenAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
