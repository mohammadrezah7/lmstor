from datetime import datetime


def university_info(request):
    return {
        'university_name': 'دانشگاه',
        'current_year': datetime.now().year,
        'site_description': 'سامانه جامع مدیریت دانشگاه',
    }