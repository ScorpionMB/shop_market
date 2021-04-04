from django import template

register = template.Library()

@register.filter
def make_russian(value, slug):
    if value % 10 == 1 and value % 100 != 11:
        return '%d %s' % (value, slug)
    if value % 10 == 0 or value % 10 > 4 and value % 10 < 10 or value % 100 > 4 and value % 100 < 20:
        return '%d %sов' % (value, slug)
    else:
        return '%d %sа' % (value, slug)