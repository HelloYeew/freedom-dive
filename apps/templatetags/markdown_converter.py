import markdown
from django import template

register = template.Library()


def convert_markdown(value: str) -> str:
    """Convert markdown to HTML."""
    return markdown.markdown(value, extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'toc',
                                                'attr_list'])


register.filter('convert_markdown', convert_markdown)