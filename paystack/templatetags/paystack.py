import datetime
from django import template
from django.shortcuts import reverse
from .. import settings
from paystack.utils import get_js_script

register = template.Library()


@register.inclusion_tag("paystack_button.html", takes_context=True)
def paystack_button(context, button_id="django-paystack-button",
                    currency="ngn", plan="", button_class="",
                    amount=None, ref=None, metadata=None,
                    email=None, redirect_url=None):

    metadata = str(metadata)
    new_redirect_url = redirect_url
    old_amount = amount
    new_amount = int(amount) * 100
    ref = metadata
    if not new_redirect_url:
        new_redirect_url = "{}?amount={}".format(
            reverse("paystack:verify_payment", args=[ref]), new_amount
        )

    return {
        "button_class": button_class,
        "button_id": button_id,
        "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
        "ref": ref,
        "email": email,
        "amount": new_amount,
        "old_amount": old_amount,
        "redirect_url": new_redirect_url,
        "currency": currency,
        "plan": plan,
        "js_url": get_js_script(),
    }
