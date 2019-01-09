from django import template

register = template.Library()

@register.simple_tag()
def status_color_code(code):
    if not code:
        return 'default'

    if code == 200:
        return 'success'

    if code == 301:
        return 'warning'

    return 'danger'
