import csv
import openpyxl

from bs4 import BeautifulSoup
from requests_html import HTMLSession

from constants import main_url, titles, reserved_characteristics, NUMBER_OF_THREADING, titles_without_article

session = HTMLSession()


def create_url(search_term, rozetka=False):
    search_term = search_term.replace(' ', '+').strip()
    url = main_url + search_term
    if rozetka:
        url += '&seller=rozetka'
    return url


def delete_brackets(search_term):
    return search_term[:search_term.find('(') - 1]


def create_request(url, render=False):
    resp = session.get(url)
    if render:
        while True:
            try:
                for i in range(5):
                    resp.html.render(timeout=100, sleep=5)
                break
            except:
                continue
    soup = BeautifulSoup(resp.html.html, 'lxml')
    return soup


def get_source(soup):
    return soup.find('div', 'goods-tile__inner').find('a').get('href')


def get_product_information(soup, url):
    print(f'start work with: {url}')
    if soup.find('h1', class_='product__title'):
        name = soup.find('h1', class_='product__title').text.strip()
    else:
        name = None
    price_and_currency = soup.find('p', class_='product-price__big')
    if price_and_currency:
        price, currency = price_and_currency.text[:-1].replace('\xa0', ''), price_and_currency.find('span').text
        #text[:-1].replace('\xa0', '').strip()
        #if not price.isdigit():
         #   price = price.split(currency)[-1]
        availability = '+' if soup.find('span', class_='buy-button__label') else '-'
    else:
        price, currency, availability = None, None, False
    images = soup.find_all('img', class_='picture-container__picture')
    images = concatenate_list([image.get('src') for image in images])
    description = soup.find('div', class_='product-about__description-content')
    if description:
        description = description.text.strip()
    brand = [soup.find('dt', class_='characteristics-simple__label'),
             soup.find('dd', class_='characteristics-simple__value')]
    if all(brand):
        try:
            brand[0], brand[1] = brand[0].find('strong').text, brand[1].find('span').text
        except:
            brand = [None, None]
    else:
        brand = [None, None]
    if soup.find('a', class_='product-about__all-link'):
        characteristics = get_characteristics(soup)
    else:
        characteristics = [None]
    return [name, price, currency, images, description, availability, brand[0], None, brand[1]] + characteristics


def concatenate_list(list_):
    string_ = ''
    for el in list_:
        string_ += f'{el}; '
    return string_.strip()[:-1]


def product_filter(product):
    for index in range(len(product)-1):
        if type(product[index]) == str:
            product[index] = product[index].replace('\xa0', ' ')
    return product


def get_characteristics(soup):
    names_and_parameters_list = []
    characteristic_url = soup.find('a', class_='product-about__all-link').get('href')
    soup = create_request(characteristic_url)
    names_and_parameters = soup.find_all('div', class_='characteristics-full__item')
    for el in names_and_parameters:
        if el.find('span'):
            name = el.find('span').text.strip()
        parameters = el.find_all('span', class_='ng-star-inserted')
        if not parameters:
            parameters = el.find_all('a')
        parameters = concatenate_list([parameter.text for parameter in parameters])
        names_and_parameters_list.append(name)
        names_and_parameters_list.append(None)
        names_and_parameters_list.append(parameters)
    return names_and_parameters_list


def check_type_of_page(soup):
    if soup.find('div', class_='catalog-empty'):
        return 'page is empty'
    elif soup.find('div', class_='rz-search-relqueries-title ng-star-inserted'):
        return 'not all words in result'
    #elif soup.find('div', class_='goods-tile__inner'):
     #   return 'page with sources'
    elif soup.find('h1', class_='catalog-heading ng-star-inserted'):
        return 'page with sources'
    elif soup.find('h1', class_='product__title'):
        return 'product page'
    else:
        return 'unreal page'


def get_search_terms(file_name='positions.csv'):
    with open(file_name, newline='', encoding='UTF-8') as file:
        reader = list(csv.reader(file))[1:]
        return reader


def write_titles(file_name, article=True):
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(titles) if article else writer.writerow(titles_without_article)


def update_information(file_name, product):
    with open(file_name, 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(product_filter(product))
        if file_name == 'not_found.csv':
            print(f'{product[0]} was add to {file_name}')
        else:
            print(f'{product[0]} was add to {file_name}')


def get_and_write_product(file_name, soup, url, vendor_code):
    product = [vendor_code] + get_product_information(soup, url)
    update_information(file_name, product)


def create_file_name(url_name, suggested_name):
    file_name = ''
    if 'rozetka' in url_name:
        file_name += 'rozetka/'
    if 'without_brackets' in url_name:
        file_name += 'without_brackets.csv'
        return file_name
    else:
        file_name += suggested_name + '.csv'
        return file_name


def main_func(search_list):
    for search_term, vendor_code in search_list:
        print(f'{search_term} was start finding')
        product = {'search_terms_searching': not search_term.isdigit() and search_term,
                   'vendor_code_searching': not vendor_code.isdigit() and vendor_code.split('=')[-1],
                   'search_term_url_rozetka': create_url(search_term, rozetka=True),
                   'vendor_code_url_rozetka': create_url(vendor_code, rozetka=True),
                   'search_term_url': create_url(search_term),
                   'vendor_code_url': create_url(vendor_code.split('=')[-1]),
                   'without_brackets_url_rozetka': create_url(delete_brackets(search_term), rozetka=True),
                   'without_brackets_url': create_url(delete_brackets(search_term))}
        search_turn = (product.get('search_term_url_rozetka') if product.get('search_terms_searching') else None,
                       product.get('vendor_code_url_rozetka') if product.get('vendor_code_searching') else None,
                       product.get('search_term_url') if product.get('search_terms_searching') else None,
                       product.get('vendor_code_url') if product.get('vendor_code_searching') else None,
                       product.get('without_brackets_url_rozetka') if product.get('search_terms_searching') else None,
                       product.get('without_brackets_url') if product.get('search_terms_searching') else None)
        url_list = [url for url in search_turn if url]
        if not url_list:
            update_information('not_found.csv', [search_term, vendor_code])

        for url in url_list:
            print(f'finding {search_term} with {url}...')
            url_name = [name for name, search_url in product.items() if url == search_url][0]
            soup = create_request(url, render=True)
            type_of_page = check_type_of_page(soup)
            while type_of_page == 'unreal page':
                print(url)
                print('trying again')
                soup = create_request(url, render=True)
                type_of_page = check_type_of_page(soup)
            if type_of_page == 'product page':
                suggested_name = 'good_result'
                file_name = create_file_name(url_name, suggested_name)
                get_and_write_product(file_name, soup, url, vendor_code)
                break
            elif type_of_page == 'page with sources' or type_of_page == 'not all words in result':
                product_url = get_source(soup)
                product_soup = create_request(product_url)
                suggested_name = 'not_so_good_result' if type_of_page == 'page with sources' else 'bad_result'
                file_name = create_file_name(url_name, suggested_name)
                get_and_write_product(file_name, product_soup, product_url, vendor_code)
                break
            elif url == url_list[-1]:
                update_information('not_found.csv', [search_term, vendor_code])
            if type_of_page == 'page is empty':
                continue
            else:
                print(type_of_page)
                print('lol, its unreal, something wrong')


def create_thread_list(search_list):
    thread_list = []
    for thread_number in range(1, NUMBER_OF_THREADING+1):
        last_index = len(search_list)//NUMBER_OF_THREADING * thread_number
        first_index = last_index - len(search_list)//NUMBER_OF_THREADING
        thread_list.append(search_list[first_index:last_index])
    if len(search_list) != last_index:
        thread_list.append(search_list[last_index:])
    return thread_list


def get_sources_upd(soup):
    sources = [el.get('href') for el in soup.find_all('a', class_='goods-tile__picture ng-star-inserted')]
    return sources


def write_to_excel(data, filename):
    data = [titles_without_article]+data
    wb = openpyxl.Workbook()
    sheet = wb.active
    for row in data:
        sheet.append(row)
    wb.save(filename)
