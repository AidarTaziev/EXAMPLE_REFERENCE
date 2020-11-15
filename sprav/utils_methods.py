from .models import *


def get_all_selects_data():
    """
    Возвращает заполненый словарь со значениями фильтров - основной страницы поиска
    :return: словарь со значениями фильтров
    """

    FILTERS_TABLES = {
        "application_categorys": ApplicationCategorys,
        "applications": Applications,
        "polymers_types": Types,
        "polymers_subtypes": Subtypes,
        "copolymers": Copolymers,
        "colors": Colors,
        "plants": Plants,
        "obtaining_methods": ObtainingMethods,
        "processing_methods": ProcessingMethods
    }

    return {selects_name: table.objects.all().order_by('name').values() for selects_name, table in FILTERS_TABLES.items()}


def get_all_polymers_for_type(type_id):
    return Polymers.objects.filter(subtype__type=type_id).values('id', 'shortcode').order_by('shortcode')