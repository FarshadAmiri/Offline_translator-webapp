from django import template

register = template.Library()

@register.filter
def fa_digits(text):
    persian_digits = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹']
    english_digits = ['0','1','2','3','4','5','6','7','8','9']
    for i in range(len(english_digits)):
        text = str(text).replace(english_digits[i], persian_digits[i])
    return text