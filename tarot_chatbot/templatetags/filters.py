from django import template

register = template.Library()

@register.filter
def card_image_filename(card_name):
    # Strip leading/trailing spaces and replace inner spaces with underscores
    return card_name.strip().replace(' ', '_') + '.jpg'