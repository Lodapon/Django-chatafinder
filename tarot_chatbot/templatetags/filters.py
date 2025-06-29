from django import template

register = template.Library()

@register.filter
def card_image_filename(card_name):
    return card_name.replace(' ', '_') + ".jpg"