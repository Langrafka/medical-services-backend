import logging
import os

import requests
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    name="send_telegram_message",
    autoretry_for=(requests.exceptions.RequestException,),
    retry_kwargs={"max_retries": 5},
    retry_backoff=True,
)
def send_telegram_notification_task(bot_type: str, message: str, reply_markup=None):
    """
    Universal task for sending telegram notification.
    :param bot_type: ADMIN/ORDER
    :param message: str with telegram message
    :param reply_markup: optional, reply markup
    :return: None, just sends telegram message
    """
    if bot_type == "admin":
        telegram_bot_token = os.environ.get("TELEGRAM_ADMIN_BOT_TOKEN")
        telegram_chat_id = os.environ.get("TELEGRAM_ADMIN_CHAT_ID")
    else:
        telegram_bot_token = os.environ.get("TELEGRAM_ORDER_BOT_TOKEN")
        telegram_chat_id = os.environ.get("TELEGRAM_ORDER_CHAT_ID")

    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message,
        "parse_mode": "HTML",
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
    except Exception as e:
        logger.exception(e)
        raise e
