from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import bleach

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def safe_comment(value,autoescape=True):
    tags = ['p','strong','em', 'u', 's', 'sub', 'sup', 'a', 'img', 'hr', 'span']
    attrs = {'img': ['alt', 'src'], 'a': ['href']}
    return mark_safe(bleach.clean(value, tags=tags, attributes=attrs))