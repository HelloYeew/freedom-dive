from django import template

register = template.Library()


def format_note_type_name(note_type: str) -> str:
    """
    Format the name of a note type from the database by remove " count" from the end.
    :param note_type: The name of the note type.
    """
    return note_type.replace(' Count', '').replace(' count', '')


register.filter('format_note_type_name', format_note_type_name)
