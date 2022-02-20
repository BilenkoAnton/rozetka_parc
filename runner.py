import csv

from constants import list_of_files
from functions import delete_brackets, create_request, get_and_write_product
from functions import get_source, create_url, check_type_of_page, create_file_name
from functions import get_search_terms, write_titles, update_information


for file in list_of_files[:-1]:
    write_titles(file)
    write_titles('rozetka/' + file)
with open('not_found.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название', 'Артикул'])

search_terms = get_search_terms()

for search_term, vendor_code in search_terms:
    product = {'search_terms_searching': not search_term.isdigit() and search_term,
               'vendor_code_searching': not vendor_code.isdigit() and vendor_code,
               'search_term_url_rozetka': create_url(search_term, rozetka=True),
               'vendor_code_url_rozetka': create_url(vendor_code, rozetka=True),
               'search_term_url': create_url(search_term),
               'vendor_code_url': create_url(vendor_code),
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
