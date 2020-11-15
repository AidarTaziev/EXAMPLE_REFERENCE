def get_search_conditions(search_filters):
    """
    Метод принимает поисковые фильтры(параметры адресной строки) и возвращает заполненный словарь с условиями поиска для queryset.
    :param search_filters: словарь с поисковыми фильтрами(параметр GET и его значение)
    :return: словарь с условиями поиска
    """

    search_conditions = {}
    for key, value in search_filters.items():
        if value and value != 'Любой':
            if key == "shortcode":
                value = ' '.join(value.split())
                search_conditions['shortcode__icontains'] = value

            elif key == "ptr_left":
                try:
                    ptr_left = float(value.replace(',', '.'))
                    search_conditions['ptr__gte'] = ptr_left
                except Exception as ex:
                    pass

            elif key == "ptr_right":
                try:
                    ptr_right = float(value.replace(',', '.'))
                    search_conditions['ptr__lte'] = ptr_right
                except Exception as ex:
                    pass

            elif key == "ptr":
                try:
                    ptr = float(value)

                    ptrLeft = ptr - (ptr * 15 / 100)
                    ptrRight = ptr + (ptr * 15 / 100)

                    search_conditions['ptr__gte'] = ptrLeft
                    search_conditions['ptr__lte'] = ptrRight

                except Exception as ex:
                    pass

            elif key == "density_left":
                try:
                    t_vika_left = float(value.replace(',', '.'))
                    search_conditions['density__gte'] = t_vika_left
                except Exception as ex:
                    pass

            elif key == "density_right":
                try:
                    t_vika_right = float(value.replace(',', '.'))
                    search_conditions['density__lte'] = t_vika_right
                except Exception as ex:
                    pass

            elif key == "density":

                polyethyleneIds = [1, 2, 19]
                try:
                    density = float(value.replace(',', '.'))

                    if type in polyethyleneIds:
                        densityLeft = density - (density * 5 / 100)
                        densityRight = density + (density * 5 / 100)

                        search_conditions['density__gte'] = densityLeft
                        search_conditions['density__lte'] = densityRight

                    else:
                        search_conditions['density'] = density

                except Exception as ex:
                    pass

            elif key == "t_vika_left":
                try:
                    t_vika_left = int(float(value.replace(',', '.')))
                    search_conditions['t_vika__gte'] = t_vika_left
                except Exception as ex:
                    pass

            elif key == "t_vika_right":
                try:
                    t_vika_right = int(float(value.replace(',', '.')))
                    search_conditions['t_vika__lte'] = t_vika_right
                except Exception as ex:
                    pass

            elif key== "t_vika":

                polystyreneId = 6

                try:
                    t_vika = int(value)

                    if type == polystyreneId:
                        t_vikaLeft = t_vika - (t_vika * 10 / 100)
                        t_vikaRight = t_vika + (t_vika * 10 / 100)

                        search_conditions['t_vika__gte'] = t_vikaLeft
                        search_conditions['t_vika__lte'] = t_vikaRight

                    else:
                        search_conditions['t_vika'] = t_vika

                except Exception as ex:
                    pass
            elif key == "application_category":
                value_list = value.split(',')
                if value_list:
                    search_conditions['applications__category__in'] = value_list
                else:
                    search_conditions['applications__category'] = value

            elif key == "application":
                value_list = value.split(',')
                if value_list:
                    search_conditions['applications__in'] = value_list
                else:
                    search_conditions['applications'] = value

            elif key == "type":
                value_list = value.split(',')
                if value_list:
                    search_conditions['subtype__type__in'] = value_list
                else:
                    search_conditions['subtype__type'] = value

            elif key == "subtype":
                value_list = value.split(',')
                if value_list:
                    search_conditions['subtype__in'] = value_list
                else:
                    search_conditions['subtype'] = value

            elif key == "copolymer":
                value_list = value.split(',')
                if value_list:
                    search_conditions['copolymer__in'] = value_list
                else:
                    search_conditions['copolymer'] = value

            elif key == "color":
                value_list = value.split(',')
                if value_list:
                    search_conditions['color__in'] = value_list
                else:
                    search_conditions['color'] = value

            elif key == "plant":
                value_list = value.split(',')
                if value_list:
                    search_conditions['plants__in'] = value_list
                else:
                    search_conditions['plants'] = value

            elif key == "obtaining_method":
                value_list = value.split(',')
                if value_list:
                    search_conditions['obtaining_methods__in'] = value_list
                else:
                    search_conditions['obtaining_methods'] = value

            elif key == "processing_method":
                value_list = value.split(',')
                if value_list:
                    search_conditions['processing_methods__in'] = value_list
                else:
                    search_conditions['processing_methods'] = value

    return search_conditions
