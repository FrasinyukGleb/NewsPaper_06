from django import template

register = template.Library()

censor_words = ['Дурак', 'Кретин', 'дурак', 'кретин', 'турнир', 'хореографии']


@register.filter()
def censor(value):
    for word in censor_words:
        if word in value:
            value = value.replace(word[1:], '*' * len(word[1:]))
    return value