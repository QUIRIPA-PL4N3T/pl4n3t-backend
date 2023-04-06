from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.encoding import escape_uri_path
from main.models import Configuration

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, viewnames, css_class='active', inactive_class='', strict_path=True, *args, **kwargs):
    request = context.get('request')
    if request is None:
        # Can't work without the request object.
        return ''
    active = False
    views = viewnames.split('||')
    for viewname in views:
        try:
            path = reverse(viewname.strip(), args=args, kwargs=kwargs)
        except NoReverseMatch:
            continue
        request_path = escape_uri_path(request.path)
        if strict_path:
            active = request_path == path
        else:
            active = request_path.find(path) == 0
        if active:
            break

    return css_class if active else inactive_class


@register.simple_tag
def site_settings(key):
    try:
        return Configuration.objects.get(key=key).value
    except Configuration.DoesNotExist:
        return ''

