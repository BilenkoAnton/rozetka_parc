from functions import create_request, get_product_information, get_sources_upd, write_to_excel

url = input('Enter url: ')

soup = create_request(url)
products_information = [get_product_information(create_request(product_url), product_url) for product_url in get_sources_upd(soup)]
write_to_excel(products_information, 'result_of_test_working.xlsx')
