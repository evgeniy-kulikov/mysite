from django import template

register = template.Library()


@register.filter
def ru_plural(value, variants):
    """
    Создание окончания для множественного числа для кириллицы
    """
    variants = variants.split(",")
    value = abs(int(value))

    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and \
            (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2

    return variants[variant]

# https://tretyakov.net/post/sklonenie-slov-vo-mnozhestvennom-chisle-v-shablonah-django/
# |ru_plural:"подписчик, подписчика, подписчиков"