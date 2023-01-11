from django import template

register = template.Library()


@register.filter
def find_replace_comma(string):
    return string.replace(',', ' ')


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
