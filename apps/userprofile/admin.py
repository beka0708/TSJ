from io import BytesIO
from reportlab.lib.colors import black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from apps.user.utils import SendSMS
from apps.userprofile.models import Request, Profile, ResidenceCertificate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image


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

def generate_certificate(pdf, certificate, y_position):
    # Регистрация шрифтов
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'font/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'font/DejaVuSans-Bold.ttf'))

    # Установка шрифта для текста
    pdf.setFont('DejaVuSans', 12)

    # Рамка для справки
    pdf.rect(50, y_position - 180, 500, 150)

    # Логотип или печать
    pdf.drawImage("avatars/logo.png", 50, y_position - 140, width=150, height=92)
    seal = Image('avatars/3.jpg', 50, 50)
    seal.drawOn(pdf, 400, y_position - 400)

    # Заголовок
    pdf.setFont('DejaVuSans-Bold', 16)
    pdf.drawString(250, y_position - 200, "СПРАВКА")
    pdf.setFont('DejaVuSans', 12)

    # Дата и номер справки
    pdf.drawString(50, y_position - 170, f"Дата: {certificate.created_date}")

    # Отступ для текста
    text_indent = 70

    # ФИО жителя
    pdf.drawString(text_indent, y_position - 220, f"Выдана гражданину: {certificate.owner_name}")

    # Адрес
    pdf.drawString(text_indent, y_position - 240, f"в том что он (она) действительно проживает по адресу: {certificate.address}")

    # Разделительная линия
    pdf.setLineWidth(1)
    pdf.setStrokeColor(black)
    pdf.line(text_indent, y_position - 260, 550, y_position - 260)

    # ФИО менеджера и дата создания
    pdf.drawString(text_indent, y_position - 280, f"Справка выдана: {certificate.created_date}, от должностного лица: {certificate.manager}")

    # Линии для подписи
    pdf.line(text_indent, y_position - 350, 300, y_position - 350)
    pdf.drawString(text_indent, y_position - 360, "Подпись гражданина")

    pdf.line(400, y_position - 350, 600, y_position - 350)
    pdf.drawString(400, y_position - 360, "Подпись должностного лица")


@admin.register(ResidenceCertificate)
class ResidenceCertificateAdmin(admin.ModelAdmin):
    actions = ['generate_pdf']

    def generate_pdf(self, request, queryset):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        y_position = 750

        for certificate in queryset:
            generate_certificate(pdf, certificate, y_position)
            y_position -= 400

        pdf.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificates.pdf"'
        return response

    generate_pdf.short_description = "Сгенерировать PDF для выбранных справок"