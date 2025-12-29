from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def user_avatar(context):
   return mark_safe(f"""
<div class="avatar">
               <div class="w-10 rounded-full">
                  <img src="{context.request.user.avatar.url}"/>
               </div>
            </div>
""")
