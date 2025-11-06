from django import template
register = template.Library()

@register.filter
def youtube_embed_url(url):
    if url and 'watch?v=' in url:
        video_id = url.split('watch?v=')[-1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    return url