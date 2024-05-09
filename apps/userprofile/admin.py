from io import BytesIO
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import path, reverse
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.encoding import smart_str
from apps.user.utils import SendSMS
from apps.userprofile.models import Request, Profile, ResidentHistory, ResidenceCertificate
from django.contrib import messages
from reportlab.pdfgen import canvas

User = get_user_model()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'address', 'phone_number')
    search_fields = ('user__name', 'user__email', 'user__address', 'user__phone_number')
    list_filter = ('user__name', 'user__email', 'user__address', 'user__phone_number')

    def email(self, obj):
        return obj.user.email if obj.user.email else "Нет email"

    def address(self, obj):
        return obj.user.address if obj.user.address else "Нет адреса"

    def phone_number(self, obj):
        return obj.user.phone_number if obj.user.phone_number else "Нет телефона"


class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "name_owner",
        "tsj",
        "number_flat",
        "name",
        "email",
        "phone_number",
        "created_date",
        "status",
    )
    search_fields = (
        "name_owner__user__name",
        "tsj__name",
        "number_flat__house__name_block",
        "name",
        "email",
        "phone_number",
    )
    list_filter = ("tsj", "status")
    readonly_fields = ("created_date",)

    # def get_urls(self):
    #     urls = super(RequestAdmin, self).get_urls()
    #     custom_url = [
    #         path('get_userprofile/<int:object_id>/', self.admin_site.admin_view(self.get_userprofile),
    #              name='get_userprofile'),
    #     ]
    #     return custom_url + urls
    #
    # def get_userprofile(self, request, object_id):
    #     user_request = Request.objects.get(pk=object_id)
    #     user_request.status = 'approved'
    #     user_request.save()
    #     if User.objects.filter(phone_number=user_request.phone_number).exists():
    #         messages.error(request,
    #                        f"Пользователь с номером {request.phone_number} уже существует.")
    #         return redirect("admin:apps_userprofile_request")
    #
    #     try:
    #         user = User.objects.create_user(
    #             role='TENANT',
    #             email=request.email,
    #             name=request.name,
    #             phone_number=request.phone_number,
    #             is_active=True,
    #             password=user_request.verification_code,
    #         )
    #         user.save()
    #       # SendSMS.send_confirmation_sms(user)
    #     except Exception as e:
    #         messages.error(request, f"Ошибка при создании пользователя: {str(e)}")
    #         return redirect("admin:apps_userprofile_request")


admin.site.register(Request, RequestAdmin)
admin.site.register(ResidentHistory)


# @admin.register(ResidenceCertificate)
# class ResidenceCertificateAdmin(admin.ModelAdmin):
#     actions = ['generate_pdf']
#
#     def generate_pdf(self, request, queryset):
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="certificates.pdf"'
#
#         buffer = BytesIO()
#         p = canvas.Canvas(buffer)
#
#         for certificate in queryset:
#             textobject = p.beginText()
#             textobject.setTextOrigin(10, 730)
#             textobject.setFont("Helvetica", 14)
#
#             text = f"Справка об местожительстве\n\n" \
#                    f"ФИО жителя: {certificate.owner_surname}\n" \
#                    f"Адрес: {certificate.address}\n" \
#                    f"ФИО менеджера: {certificate.created_by}\n" \
#                    f"Дата создания: {certificate.issue_date}"
#
#             textobject.textLine(text)
#             p.drawText(textobject)
#             p.showPage()
#
#         p.save()
#         buffer.seek(0)
#         response.write(buffer.getvalue())
#
#         return response
#     generate_pdf.short_description = "Сгенерировать PDF для выбранных справок"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - -  - - - -

# @admin.register(ResidenceCertificate)
# class ResidenceCertificateAdmin(admin.ModelAdmin):
#     actions = ['generate_pdf']
#
#     def generate_pdf(self, request, queryset):
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="certificates.pdf"'
#
#         for certificate in queryset:
#             html = render_to_string('admin/certificate_template.html',
#                                     {'certificate': certificate}, request=request)
#             pisa_status = pisa.CreatePDF(html.encode('UTF-8'), dest=response, encoding='UTF-8')
#             # pdf = pisa.CreatePDF(smart_str(html), dest=response, encoding='UTF-8')
#             if pisa_status.err:
#                 return HttpResponse('Ошибка при создании PDF', status=400)
#
#         return response
#     generate_pdf.short_description = "Сгенерировать PDF для выбранных справок"

# - - - - - - - - - - - -- -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - -

# @admin.register(ResidenceCertificate)
# class ResidenceCertificateAdmin(admin.ModelAdmin):
#     actions = ['generate_pdf']
#
#     def generate_pdf(self, request, queryset):
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer, pagesize=letter)
#
#         # Добавим шрифт DejaVuSans
#         pdfmetrics.registerFont(TTFont('DejaVuSans', 'font/DejaVuSans.ttf'))
#
#         # Установим шрифт для текста
#         pdf.setFont('DejaVuSans', 12)
#
#         # Начинаем создание PDF
#         pdf.drawString(100, 750, "Справка об местожительстве")
#
#         y_position = 700  # Начальная позиция Y
#
#         for certificate in queryset:
#             y_position -= 20
#             pdf.drawString(100, y_position, f"ФИО жителя: {certificate.owner_surname}")
#             y_position -= 20
#             pdf.drawString(100, y_position, f"Адрес: {certificate.address}")
#             y_position -= 20
#             pdf.drawString(100, y_position, f"ФИО менеджера: {certificate.created_by}")
#             y_position -= 20
#             pdf.drawString(100, y_position, f"Дата создания: {certificate.issue_date}")
#
#         pdf.showPage()
#         pdf.save()
#
#         buffer.seek(0)
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="certificates.pdf"'
#         return response
#
#     generate_pdf.short_description = "Сгенерировать PDF для выбранных справок"

@admin.register(ResidenceCertificate)
class ResidenceCertificateAdmin(admin.ModelAdmin):
    actions = ['generate_pdf']

    def generate_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificates.pdf"'

        for certificate in queryset:
            html = render_to_string('admin/certificate_template.html', {'certificate': certificate})
            pisa_status = pisa.CreatePDF(html, dest=response, encoding='UTF-8', font_path='font/DejaVuSans.ttf')
            if pisa_status.err:
                return HttpResponse('Ошибка при создании PDF', status=400)

        return response

    generate_pdf.short_description = "Сгенерировать PDF для выбранных справок"

