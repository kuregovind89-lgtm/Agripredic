"""
WhatsApp / SMS alert dispatch via Twilio.

If TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN aren't set in .env, this module
no-ops (logs to console) instead of failing, so the rest of the app keeps
working without a Twilio account. Once you add real credentials, messages
are sent for real -- no other code changes needed.

Twilio free trial: https://www.twilio.com/try-twilio
WhatsApp sandbox setup: https://www.twilio.com/docs/whatsapp/sandbox
"""
import os
import logging

logger = logging.getLogger("agripredic.alerts")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886").strip()
TWILIO_SMS_FROM = os.getenv("TWILIO_SMS_FROM", "").strip()

_client = None


def _get_client():
    global _client
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return None
    if _client is None:
        from twilio.rest import Client  # imported lazily; only needed if configured
        _client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    return _client


def _configured():
    return bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN)


def send_whatsapp_alert(to_phone: str, message: str) -> bool:
    """to_phone should be in E.164 format, e.g. +919876543210."""
    if not to_phone:
        return False
    client = _get_client()
    if not client:
        logger.info(f"[WhatsApp alert - Twilio not configured, skipped] to={to_phone}: {message}")
        return False
    try:
        client.messages.create(from_=TWILIO_WHATSAPP_FROM, to=f"whatsapp:{to_phone}", body=message)
        return True
    except Exception as e:  # noqa: BLE001 - alert delivery must never crash the request
        logger.error(f"WhatsApp send failed: {e}")
        return False


def send_sms_alert(to_phone: str, message: str) -> bool:
    if not to_phone:
        return False
    client = _get_client()
    if not client or not TWILIO_SMS_FROM:
        logger.info(f"[SMS alert - Twilio not configured, skipped] to={to_phone}: {message}")
        return False
    try:
        client.messages.create(from_=TWILIO_SMS_FROM, to=to_phone, body=message)
        return True
    except Exception as e:  # noqa: BLE001
        logger.error(f"SMS send failed: {e}")
        return False


def send_risk_alert(user, location: str, risk_type: str, risk_pct: float, prefer_whatsapp: bool = True):
    """Convenience wrapper used by risk_routes.py / predict_routes.py to notify
    a farmer about a high-risk condition via their saved phone number."""
    if not getattr(user, "phone", None):
        return False
    message = (
        f"AgriPredic Alert: {risk_type} risk is {risk_pct}% in {location}. "
        f"Please take preventive action for your crop."
    )
    if prefer_whatsapp:
        sent = send_whatsapp_alert(user.phone, message)
        if sent:
            return True
    return send_sms_alert(user.phone, message)
