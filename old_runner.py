import csv

from constants import list_of_files
from functions import delete_brackets, create_request, get_and_write_product
from functions import get_source, create_request_and_check_type_of_page
from functions import get_search_terms, write_titles

for file in list_of_files[:-1]:
    write_titles(file)
    write_titles('rozetka/' + file)
with open('not_found.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название', 'Артикул'])
search_terms = get_search_terms()

for search_term, vendor_code in search_terms:
    url, soup, type_of_page = create_request_and_check_type_of_page(search_term, render=True)
    print(type_of_page, url)
    if type_of_page == 'page is empty':
        url, soup, type_of_page = create_request_and_check_type_of_page(vendor_code.split('=')[-1], render=True)
        if type_of_page == 'page is empty':
            url, soup, type_of_page = create_request_and_check_type_of_page(delete_brackets(search_term), render=True)
            if type_of_page == 'page is empty':
                with open('not_found.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([search_term, vendor_code])
                    print(f'{search_term} not found')
                continue
    if type_of_page == 'product page':
        file_name = 'good_result.csv'
        get_and_write_product(file_name, soup, url, vendor_code)
    elif type_of_page == 'page with sources' or type_of_page == 'not all words in result':
        product_url = get_source(soup)
        product_soup = create_request(product_url)
        file_name = 'not_so_good_result.csv' if type_of_page == 'page with sources' else 'bad_result.csv'
        get_and_write_product(file_name, product_soup, product_url, vendor_code)
    else:
        print(type_of_page)
        print('lol, its unreal, something wrong')

for file in list_of_files:
    with open(file, newline='', encoding='UTF-8') as file:
        reader = list(csv.reader(file))[1:]
    print(f'{file}:{len(reader)} products')
