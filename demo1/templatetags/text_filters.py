from django import template

register = template.Library()

@register.filter(name='truncate_title')

def truncate_title(value, max_length=18):
    """
    限制标题显示的长度。如果字符数超过最大长度，用...替换。
    英文按一个字符计算，中文按两个字符计算。
    """
    total_length = 0
    result = []

    for char in value:
        # 英文字符计1，中文字符计2
        total_length += 2 if ord(char) > 127 else 1

        if total_length <= max_length:
            result.append(char)
        else:
            break

    return ''.join(result) + ('...' if total_length > max_length else '')
