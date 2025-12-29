from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def tx_amount_tailwind(tx, user):
    """
    根据 user 是 sender / recipient
    生成带 Tailwind class 的 <span>
    """
    if not user or not tx:
        return ""

    if tx.sender_id == user.id:
        css = "text-red-500"
        amount = -tx.amount
    else:
        css = "text-green-500"
        amount = tx.amount

    return format_html(
        '<span class="{}">{}</span>',
        css,
        amount
    )