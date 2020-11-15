

#TODO: ИСПОЛЬЗУЮ ЕГО ВМЕСТО ФОРМЫ
def valid_search_filters(search_filters):
    is_valid = True
    errors_list = []

    if 'ptr_left' in search_filters and 'ptr_right' in search_filters:
        try:
            if float(search_filters['ptr_left'].replace(',', '.')) > float(
                    search_filters['ptr_right'].replace(',', '.')):
                is_valid = False
                errors_list.append('Левое значение ПТР не может быть больше правого')
        except ValueError as ex:
            is_valid = False
            errors_list.append('Интервал значений для ПТР должен быть указан в числовом виде')

    if 'density_left' in search_filters and 'density_right' in search_filters:
        try:
            if float(search_filters['density_left'].replace(',', '.')) > float(
                    search_filters['density_right'].replace(',', '.')):
                is_valid = False
                errors_list.append('Левое значение Плотности не может быть больше правого')
        except ValueError as ex:
            is_valid = False
            errors_list.append('Интервал значений для Плотности должен быть указан в числовом виде')

    if 't_vika_left' in search_filters and 't_vika_right' in search_filters:
        try:
            if int(float(search_filters['t_vika_left'].replace(',', '.'))) > int(
                    float(search_filters['t_vika_right'].replace(',', '.'))):
                is_valid = False
                errors_list.append('Левое значение Температуры Вика не может быть больше правого')
        except ValueError as ex:
            is_valid = False
            errors_list.append('Интервал значений для Температуры Вика должен быть указан в числовом виде')

    return is_valid, errors_list
