import json

from django.db import transaction
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from crm.models import CareerForm, ContactForm, Order, FormStatus, OrderStatus
from crm.tasks import send_telegram_notification_task


@receiver(post_save, sender=ContactForm)
def send_telegram_notification_contact_form(sender, instance, created, **kwargs):
    if created:
        ContactForm.objects.filter(pk=instance.pk).update(status=FormStatus.PENDING)
        send_telegram_notification_task.delay(
            bot_type="admin",
            message=f"New contact form: {instance.first_name} {instance.last_name} - {instance.phone}",
        )


@receiver(post_save, sender=CareerForm)
def send_telegram_notification_career_form(sender, instance, created, **kwargs):
    if created:
        CareerForm.objects.filter(pk=instance.pk).update(status=FormStatus.PENDING)
        send_telegram_notification_task.delay(
            bot_type="admin",
            message=f"New career form: {instance.first_name} {instance.last_name} - {instance.phone}",
        )


@receiver(m2m_changed, sender=Order.nurse.through)
def send_telegram_notification_order(sender, instance, action, **kwargs):
    if action == "post_add":

        def send_msg():
            instance.refresh_from_db()
            markup_data = {
                "inline_keyboard": [
                    [
                        {"text": "Accept", "callback_data": f"accept_{instance.pk}"},
                        {"text": "Reject", "callback_data": f"reject_{instance.pk}"},
                        {"text": "Done", "callback_data": f"done_{instance.pk}"},
                    ]
                ]
            }
            reply_markup_json = json.dumps(markup_data)
            message = (
                f"New order: {instance.customer.first_name} {instance.customer.last_name} - {instance.customer.phone}\n"
                f"Address: {instance.address.street} {instance.address.building} {instance.address.local if instance.address.local else ''},"
                f"{instance.address.postal_code}, {instance.address.city} \n"
                f"Nurse: {', '.join([(str(n.first_name) + ' ' + str(n.last_name)) for n in instance.nurse.all()])}\n"
                f"Order: {', '.join([str(it.service.name) + ' - ' + str(it.quantity) for it in instance.order_items.all()])}"
            )
            Order.objects.filter(pk=instance.pk).update(status=OrderStatus.PENDING)
            send_telegram_notification_task.delay(
                bot_type="order",
                message=message,
                reply_markup=reply_markup_json,
            )

        transaction.on_commit(send_msg)
