from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using its key."""
    return dictionary.get(key)

@register.filter
def filter_by_enrollment(grades, enrollment):
    """Filter grades by enrollment."""
    return grades.filter(enrollment=enrollment) 