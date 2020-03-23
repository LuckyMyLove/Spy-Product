import main_functions
import web_scraping
import reports
import sys

def add_product():
    print("List of supported stores: Ceneo, Steam, Muve.pl, Medicine, MediaExpert, RTV Euro AGD")

    url = input("Please provide a link to the product: ").strip()

    if main_functions.check_URL(url):
        produkt = web_scraping.get_info(url)
        print("\nYour product is: %s, his price is %s" %(produkt.title, produkt.price))

        toDo = input("Do you want to add product to Your report?(Y/N): ")
        if toDo == "Y" or toDo == 'y':
            reports.add_toRep(produkt)
        else: main_functions.clear_screen()

def refresh_report():
    reports.refresh_report()

def exit():
    sys.exit()

def no_such_action():
    print("You used the wrong option, please select again. \n")

def main():
    actions = {"1": add_product, "2": refresh_report, "3": exit}
    while True:
        print("1. Find product")
        print("2. Refresh report")
        print("3. Exit")

        selection = input("Choose option: ")
        main_functions.clear_screen()

        toDo = actions.get(selection, no_such_action)
        toDo()



if __name__ == "__main__":
    main()
