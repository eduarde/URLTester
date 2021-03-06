from django import template

register = template.Library()


@register.simple_tag()
def status_color_code(code):
    if not code:
        return 'default'

    if code == '200':
        return 'success'

    if code == '301' or code == '302':
        return 'warning'

    if code == '?':
        return 'secondary'

    return 'danger'
