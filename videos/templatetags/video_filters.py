from django import template
import re

register = template.Library()


@register.filter
def youtube_id(value):
    """
    Извлекает ID из YouTube-ссылки.
    Поддержка ссылок вида:
    - https://www.youtube.com/watch?v=abc123xyz89
    - https://youtu.be/abc123xyz89
    """
    if not value:
        return ''

    # Ищем ID YouTube-видео
    match = re.search(r'(v=|youtu\.be/)([a-zA-Z0-9_-]{11})', value)

    if match:
        return match.group(2)
    return ''
