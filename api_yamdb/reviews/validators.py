from datetime import datetime

from django.core.exceptions import ValidationError

def year_validator(value):
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(
            f'Год не может быть больше {current_year}'
        )
