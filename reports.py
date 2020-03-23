# openpyxl is required for for correctly working printing reports -> download it using "pip install openpyxl" in cmd
import pandas as pd
import os.path
from web_scraping import get_info
from main_functions import clear_screen


def add_toRep(product):
    products_list = []
    new_product = [product.url, product.title, product.price, product.date]

    if os.path.exists('./report.xlsx'):
        products_list = pd.read_excel(r'./report.xlsx').fillna('').values.tolist()
        products_list = remove_duplicates(products_list)

    for product_row in products_list:
        if new_product[0] == product_row[0]:
            clear_screen()
            print("Product is already in report")
            return

    products_list.append(new_product)
    report_df = pd.DataFrame(products_list, columns=['URL', 'Title', 'Price', 'Download date'])

    try:
        report_df.to_excel(r'./report.xlsx', index=False)
        clear_screen()
        print("The product has been added to the report")
    except PermissionError:
        print("There is no access to the report. Perhaps report.xlsx is opend")


def refresh_report():
    if not os.path.exists('./report.xlsx'):
        clear_screen()
        print("There is no report to refresh \n")

    products_list = pd.read_excel(r'./report.xlsx').fillna('').values.tolist()
    products_list = remove_duplicates(products_list)
    new_products_list = []

    for product in products_list:
        current_row = get_info(str(product[0]))
        new_products_list.append([current_row.url, current_row.title, current_row.price, current_row.date])

    report_df = pd.DataFrame(new_products_list, columns=['URL', 'Title', 'Price', 'Download date'])

    try:
        report_df.to_excel(r'./report.xlsx', index=False)
        clear_screen()
        print("The report has been updated successfully")
    except PermissionError:
        print("There is no access to the report. Perhaps report.xlsx is opend")


def remove_duplicates(list):
    for product in list:
        if product[0] == '':
            list.remove(product)
            remove_duplicates(list)
            break
    return list