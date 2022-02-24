import csv

from constants import list_of_files
from functions import get_search_terms, main_func

list_of_lists = []
names_of_files = []
for file in list_of_files[:-1]:
    list_of_lists.append(get_search_terms(f'rozetka/{file}'))
    names_of_files.append(f'rozetka/{file}')
    list_of_lists.append(get_search_terms(f'{file}'))
    names_of_files.append(f'{file}')
list_of_lists.append(get_search_terms('not_found.csv'))
names_of_files.append('not_found.csv')
lens_of_files = [len(el) for el in list_of_lists]
#print(tuple(zip(names_of_files, lens_of_files)))
vendor_codes = [el[1] for el in get_search_terms()]

list_of_vendor_codes = []
for files in list_of_lists[:-1]:
    for file in files:
        if file:
            #print(file)
            list_of_vendor_codes.append(file[0])

for file in list_of_lists[-1]:
    if file:
        #print(file)
        list_of_vendor_codes.append(file[1])

#print(len(list_of_vendor_codes))
print(sum(lens_of_files))

for vendor_code in vendor_codes:
    if vendor_code and vendor_code not in list_of_vendor_codes:
        print(vendor_code)

#main_func([['WA 6081   (412)', '412 = WA6081'], ['LS895     (PURFLUX)', 'LS895']])
#todo: characteristics for good result
#todo: brand
#todo: add 2 products
#todo: lie in avaible
