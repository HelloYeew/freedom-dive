from django import template

register = template.Library()


def get_star_color(difficulty_rating: float) -> dict:
    """Return a dict containing the background color and text color for a star rating badge."""
    if difficulty_rating <= 1.5:
        background_color = 'rgb(65, 184, 255)'
    elif 1.5 < difficulty_rating <= 2.0:
        background_color = 'rgb(65, 215, 235)'
    elif 2.0 < difficulty_rating <= 2.25:
        background_color = 'rgb(77, 252, 186)'
    elif 2.25 < difficulty_rating <= 2.5:
        background_color = 'rgb(123, 251, 70)'
    elif 2.5 < difficulty_rating <= 2.75:
        background_color = 'rgb(160, 246, 73)'
    elif 2.75 < difficulty_rating <= 3.0:
        background_color = 'rgb(197, 242, 80)'
    elif 3.0 < difficulty_rating <= 3.25:
        background_color = 'rgb(241, 236, 83)'
    elif 3.25 < difficulty_rating <= 3.5:
        background_color = 'rgb(248, 211, 84)'
    elif 3.5 < difficulty_rating <= 3.75:
        background_color = 'rgb(248, 187, 87)'
    elif 3.75 < difficulty_rating <= 4.0:
        background_color = 'rgb(254, 161, 90)'
    elif 4.0 < difficulty_rating <= 4.25:
        background_color = 'rgb(255, 138, 92)'
    elif 4.25 < difficulty_rating <= 4.5:
        background_color = 'rgb(255, 117, 90)'
    elif 4.5 < difficulty_rating <= 4.75:
        background_color = 'rgb(255, 103, 97)'
    elif 4.75 < difficulty_rating <= 5.0:
        background_color = 'rgb(255, 95, 95)'
    elif 5.0 < difficulty_rating <= 5.25:
        background_color = 'rgb(255, 83, 102)'
    elif 5.25 < difficulty_rating <= 5.5:
        background_color = 'rgb(255, 72, 102)'
    elif 5.5 < difficulty_rating <= 5.75:
        background_color = 'rgb(253, 54, 103)'
    elif 5.75 < difficulty_rating <= 6.0:
        background_color = 'rgb(253, 54, 103)'
    elif 6.0 < difficulty_rating <= 6.25:
        background_color = 'rgb(209, 64, 132)'
    elif 6.25 < difficulty_rating <= 6.5:
        background_color = 'rgb(166, 73, 157)'
    elif 6.5 < difficulty_rating <= 6.75:
        background_color = 'rgb(122, 83, 192)'
    elif 6.75 < difficulty_rating <= 7.0:
        background_color = 'rgb(87, 92, 213)'
    elif 7.0 < difficulty_rating <= 7.25:
        background_color = 'rgb(66, 73, 190)'
    elif 7.25 < difficulty_rating <= 7.5:
        background_color = 'rgb(50, 55, 168)'
    elif 7.5 < difficulty_rating <= 7.75:
        background_color = 'rgb(36, 39, 150)'
    elif 7.75 < difficulty_rating <= 7.99:
        background_color = 'rgb(22, 25, 144)'
    else:
        background_color = 'rgb(0, 0, 0)'
    if difficulty_rating <= 6.5:
        color = 'rgb(51, 58, 61)'
    else:
        color = 'rgb(255, 215, 93)'
    return {
        'background_color': background_color,
        'color': color
    }
        

register.filter('get_star_color', get_star_color)