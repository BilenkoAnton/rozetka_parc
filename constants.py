main_url = 'https://rozetka.com.ua/search/?text='
titles = ['Артикул', 'Имя', 'Цена',
          'Валюта', 'Картинка', 'Описание',
          'Наличие'] + ['Наименование_характеристики', 'Измерение_характеристики']*15
list_of_files = ['good_result.csv', 'not_so_good_result.csv', 'bad_result.csv', 'without_brackets.csv', 'not_found.csv']
reserved_characteristics = ('Производитель', 'Страна производитель', 'Тип', 'Гарантия',
                            'Цвет', 'Материал', 'Емкость (вес)', 'Объем', 'Консистенция')
