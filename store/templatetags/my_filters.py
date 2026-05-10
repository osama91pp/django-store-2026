from django import template

register = template.Library()

def currency(value):
    return '{:.2f} $'.format(value)

register.filter('currency', currency)