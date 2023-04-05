main_url = 'https://rozetka.com.ua/search/?text='
titles = ['Артикул', 'Имя', 'Цена',
          'Валюта', 'Картинка', 'Описание',
          'Наличие'] + ['Наименование_характеристики', 'Измерение_характеристики']*15
titles_without_article = ['Имя', 'Цена', 'Валюта', 'Картинка', 'Описание', 'Наличие'] + \
                         ['Наименование_характеристики', 'Измерение_характеристики', 'Значение_характеристики']*15
list_of_files = ['good_result.csv', 'not_so_good_result.csv', 'bad_result.csv', 'without_brackets.csv', 'not_found.csv']
reserved_characteristics = ('Страна производитель', 'Тип', 'Гарантия', 'Цвет',
                            'Материал', 'Емкость (вес)', 'Объем', 'Консистенция')
NUMBER_OF_THREADING = 4
