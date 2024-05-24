from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.views import APIView
import xml.etree.ElementTree as ET
from apps.home.models import Request_Vote_News, Flat
from apps.home.serializers import RequestVoteSerializers
from .models import DomKom, Camera, HelpInfo, PaymentType, Debt, Payment
from .payment_utils import FreedomPay
from .serializers import (
    DomKomSerializers, CameraSerializers,
    HelpInfoSerializers, PaymentSerializer,
    DebtSerializer, PaymentTypeSerializer, CreatePaymentSerializer
)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

User = get_user_model()
# freedom_pay = FreedomPay()


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class DomKomViewSet(viewsets.ModelViewSet):
    queryset = DomKom.objects.all()
    serializer_class = DomKomSerializers
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     return DomKom.objects.filter(info=user)


class HistoryRequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestVoteSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_requests = Request_Vote_News.objects.filter(user=user)
        return user_requests


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializers


class HelpInfoViewSet(viewsets.ModelViewSet):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializers


class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer


class PaymentAPI(APIView):
    payment_pay = FreedomPay()
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
        # serializer = self.serializer(data=request.data, context={'request': request})
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
    payment_pay = FreedomPay()
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            payment = Payment.objects.get(id=order_id)
        except Payment.DoesNotExist:
            return Response({'error': 'Order ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

        response_status = self.payment_pay.get_payment_status_by_order_id(payment.id)
        status_element = response_status.find('pg_status').text
        return Response({'status': status_element, 'full_response': ET.tostring(response_status, encoding='utf8').decode('utf8')}, status=200)
