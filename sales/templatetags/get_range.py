from django.template import Library

register = Library()

@register.filter
def get_range(value):
    if value < 0:
        value = value * -1
        
    return xrange(value)
