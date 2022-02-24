import csv
import multiprocessing

from constants import list_of_files
from functions import delete_brackets, create_request, get_and_write_product
from functions import get_source, create_url, check_type_of_page, create_file_name
from functions import get_search_terms, write_titles, update_information, main_func, create_thread_list


for file in list_of_files[:-1]:
    write_titles(file)
    write_titles('rozetka/' + file)
with open('not_found.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название', 'Артикул'])


search_terms = get_search_terms()
# thread_list = create_thread_list(search_terms)
# for thread in thread_list:
#     thread.start()
#     print(f'{thread} was started')

if __name__ == '__main__':
    thread_list = create_thread_list(search_terms)
    with multiprocessing.Pool() as pool:
        res = pool.map(main_func, thread_list)


