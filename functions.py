import csv
from datetime import datetime

from bs4 import BeautifulSoup
from requests_html import HTMLSession

from constants import main_url, titles, reserved_characteristics

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
        resp.html.render(timeout=100, sleep=3)
    soup = BeautifulSoup(resp.html.html, 'lxml')
    return soup


def get_source(soup):
    return soup.find('div', 'goods-tile__inner').find('a').get('href')


def get_product_information(soup, url):
    name = soup.find('h1', class_='product__title').text.strip()
    price_and_currency = soup.find('div', class_='product-prices__inner')
    if price_and_currency:
        price, currency = price_and_currency.text[:-1].replace('\xa0', '').strip(), price_and_currency.text[-1]
        if not price.isdigit():
            price = price.split(currency)[1]
        availability = '+' if bool(soup.find('span', class_='buy-button__label')) else '-'
    else:
        price, currency, availability = None, None, False
    image = soup.find('img', class_='picture-container__picture').get('src')
    description = soup.find('div', class_='product-about__description-content')
    if description:
        description = description.text.strip()
    characteristics = get_characteristics(url)
    return [name, price, currency, image, description, availability] + characteristics


def concatenate_list(list_):
    string_ = ''
    for el in list_:
        string_ += f'{el}, '
    return string_.strip()[:-1]


def product_filter(product):
    for index in range(len(product)-1):
        if type(product[index]) == str:
            product[index] = product[index].replace('\xa0', ' ')
    return product


def get_characteristics(url):
    characteristic_url = f'{url}characteristics/'
    soup = create_request(characteristic_url)
    names_and_parameters_list = [None]*len(reserved_characteristics)*2
    names_and_parameters = soup.find_all('div', class_='characteristics-full__item')
    for el in names_and_parameters:
        name = el.find('span').text.strip()
        parameters = el.find_all('span', class_='ng-star-inserted')
        if not parameters:
            parameters = el.find_all('a')
        parameters = concatenate_list([parameter.text for parameter in parameters])
        if name in reserved_characteristics:
            for index in range(len(reserved_characteristics)):
                if reserved_characteristics[index] == name:
                    index_for_name = index * 2
                    names_and_parameters_list[index_for_name] = name
                    index_for_parameter = index_for_name + 1
                    names_and_parameters_list[index_for_parameter] = parameters
        else:
            names_and_parameters_list.append(name)
            names_and_parameters_list.append(parameters)
    return names_and_parameters_list


def check_type_of_page(soup):
    if soup.find('div', class_='catalog-empty'):
        return 'page is empty'
    elif soup.find('div', class_='rz-search-relqueries-title ng-star-inserted'):
        return 'not all words in result'
    elif soup.find('div', class_='goods-tile__inner'):
        return 'page with sources'
    elif soup.find('h1', class_='product__title'):
        return 'product page'
    else:
        return 'unreal page'


def get_search_terms(file_name='positions.csv'):
    with open(file_name, newline='', encoding='UTF-8') as file:
        reader = list(csv.reader(file))[1:]
        return reader


def write_titles(file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(titles)


def update_information(file_name, product):
    with open(file_name, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(product_filter(product))
        if file_name == 'not_found.csv':
            print(f'{product[0]} was add to {file_name}')
        else:
            print(f'{product[1]} was add to {file_name}')


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
