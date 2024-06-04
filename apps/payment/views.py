from rest_framework.views import APIView
from .serializers import PaymentTypeSerializer, PaymentSerializer, CreatePaymentSerializer
from .models import PaymentType, Payment
import xml.etree.ElementTree as ET
from freedom_pay.service import FreedomPay
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.conf import settings

freedom = FreedomPay(
    settings.MERCHANT_ID,
    settings.PAY_SECRET_KEY,
    settings.PG_SUCCESS_URL,
    settings.PG_FAILURE_URL,
    settings.PG_BACK_LINK
)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class PaymentAPI(APIView):
    payment_pay = freedom
    serializer = CreatePaymentSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        payments = Payment.objects.filter(user=user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            payment_data = serializer.save()

            response_pay = self.payment_pay.init_payment_online(
                amount=payment_data.amount,
                order_id=payment_data.id,
                user_id=payment_data.user.id,
                description=payment_data.payment_type.name
            )

            root = ET.fromstring(response_pay.text)
            pg_redirect_url = root.find('pg_redirect_url').text
            return Response({'redirect': pg_redirect_url}, status=200)

        return Response({"error": "Требуются данные пользователя об платеже"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusAPIView(APIView):
    payment_pay = freedom
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            payment = Payment.objects.get(id=order_id)
        except Payment.DoesNotExist:
            return Response({'error': 'Order ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

        response_status = self.payment_pay.get_payment_status_by_order_id(payment.id)
        status_element = response_status.find('pg_status').text
        return Response(
            {'status': status_element, 'full_response': ET.tostring(response_status, encoding='utf8').decode('utf8')},
            status=200)
