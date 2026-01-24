# crm/views.py
import logging
import os

import requests
from dal import autocomplete
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from crm.models import Address, Customer, Order
from crm.serializers import CareerFormSerializer, ContactFormSerializer
from operations.models import Nurse

logger = logging.getLogger(__name__)


class ContactFormView(CreateAPIView):
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forms_throttle"
    serializer_class = ContactFormSerializer

    def perform_create(self, serializer):
        phone = serializer.validated_data.get("phone")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")

        customer, created = Customer.objects.get_or_create(
            phone=phone,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
            },
        )

        serializer.save(customer=customer)


class CareerFormView(CreateAPIView):
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forms_throttle"
    serializer_class = CareerFormSerializer


class NurseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Nurse.objects.all()
        qs = Nurse.objects.all()
        region = self.forwarded.get("region", None)
        if region:
            qs = qs.filter(region=region)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class AddressAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Address.objects.all()
        qs = Address.objects.all()
        region = self.forwarded.get("region", None)
        if region:
            qs = qs.filter(region=region)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


@method_decorator(csrf_exempt, name="dispatch")
class OrderCallback(APIView):
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forms_throttle"

    def post(self, request, *args, **kwargs):
        bot_token = os.environ.get("TELEGRAM_ORDER_BOT_TOKEN")
        data = request.data.get("callback_query", {})
        request_id = data.get("id")
        callback_string = data.get("data")

        user_info = data.get("from", {})
        first_name = user_info.get("first_name", "Unknown")

        message_obj = data.get("message", {})
        chat_id = message_obj.get("chat", {}).get("id")
        message_id = message_obj.get("message_id")
        original_text = message_obj.get("text", "")
        reply_markup = data.get("reply_markup", {})

        if callback_string:
            try:
                action_type, pk = callback_string.split("_")
                order_qs = Order.objects.filter(pk=pk)
                toast_text = "Action completed!"

                if action_type.lower() == "accept":
                    if order_qs.filter(status="ACCEPTED").exists():
                        toast_text = "Order is already accepted!"
                    else:
                        order_qs.update(status="ACCEPTED")
                        toast_text = f"Order accepted by {first_name}!"
                        new_text = f"{original_text}\n\n✅ <b>Status: Accepted by {first_name}</b>"
                elif action_type.lower() == "done":
                    order_qs.update(status="DONE")
                    toast_text = "Order done!"
                    new_text = f"{original_text}\n\n✅✅ <b>Status: Completed by {first_name}</b>"
                elif action_type.lower() == "reject":
                    order_qs.update(status="REJECTED")
                    toast_text = "Order rejected!"
                    new_text = f"{original_text}\n\n\❌ <b>Status: Rejected by {first_name}</b>"

                if request_id:
                    base_url = f"https://api.telegram.org/bot{bot_token}/"
                    requests.post(
                        url=base_url + "answerCallbackQuery",
                        json={
                            "callback_query_id": request_id,
                            "text": toast_text,
                            "show_alert": False,
                        },
                    )
                    requests.post(
                        url=base_url + "editMessageText",
                        json={
                            "chat_id": chat_id,
                            "message_id": message_id,
                            "text": new_text,
                            "reply_markup": (
                                reply_markup
                                if action_type.lower() == "reject"
                                else None
                            ),
                            "parse_mode": "HTML",
                        },
                    )
            except Exception as e:
                logger.error(f"Telegram Webhook Error: {e}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
