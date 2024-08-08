import os
import pymupdf

DIRECTORY_NAME = "statements"

class Purchase:
    def __init__(self, description, price):
        self.description = description 
        self.price = extract_price(price)

    def __str__(self):
        return f"Description: {self.description}\nPrice: {self.price}"


class Category:
    def __init__(self, cat_id, name):
        self.id = cat_id
        self.name = name
        self.amount = 0

    def __repl__(self):
        return f"{self.name}: ${self.amount}"

    def __str__(self):
        return f"{self.name}: ${self.amount}"


# Given a string, determines if it's a date
def is_date(date_string: str) -> bool:
    split_date_string = date_string.split("/")
    if split_date_string != date_string:
        for num in split_date_string:
            stripped_num = num.strip()
            if len(stripped_num) != 2 or not stripped_num.isnumeric():
                return False
        return True
    else:
        return False 


# Extract a purchase's price from the string containing it
def extract_price(price_line: str) -> float:
    try:
        return float(price_line.replace("$", "").replace(",", "").strip())
    except ValueError:
        print(f"Cannot convert {price_line} to float.")


# Given the extracted text of a Chase statement, create a list of Purchase objects
def parse_chase(text) -> list[Purchase]:
    lines = text[2].split("$ Amount")[1].split("\n")[1:] 
    purchases = []
    for i in range(0, len(lines), 3):
        if is_date(lines[i]):
            purchases.append(Purchase(lines[i+1], lines[i+2]))
        else:
            break
    return purchases


# Given the extracted text of a Discover statement, create a list of Purchase objects
def parse_discover(text) -> list[Purchase]:
    lines = text[0].split("Category")[1].split("Statement Balance is the total")[0].split("\n")
    purchases = []
    for index, line in enumerate(lines):
        # If the current line is a date, it is potentially the beginning of a new row
        if is_date(line):
            # Beginning of new line has two sequential dates. Confirm that to prevent duplicates
            if not is_date(lines[index + 1]):
                continue 
            offset = 2
            purchase_description = ""
            purchase_amount = "" 
            # Iterate through the remaining columns in the document to grab all purchase data
            while True:
                description = lines[index + offset]
                if "$" in description:
                    purchase_amount = description[2:].split(" ")[0] 
                    purchases.append(Purchase(purchase_description, purchase_amount))
                    break
                purchase_description += description
                offset += 1
    return purchases


# Given a PDF file name, extracts all text and returns a list of strings
def extract_text(file_name: str) -> list[str]:
    doc = pymupdf.open(file_name)
    text_list = []
    for page in doc:
        text_list.append(page.get_text())
    return text_list


# Get a dictionary of budget categories from the user
def get_categories() -> dict[int, Category]:
    categories = dict() 
    category_id = 1
    while True:
        new_category_name = input("Input category name, or 0 when done: ")
        for category in categories.values():
            if category.name == new_category_name: 
                print("Category name in use, try again.") 
                continue
        if new_category_name == "0":
            break
        else:
            categories[str(category_id)] = Category(category_id, new_category_name) 
            category_id += 1
    return categories


# Parse all the statements in the statement folder, return a list of Purchase objects
def parse_statements() -> list[Purchase]:
    parsed = []
    # For each file in the queue
    for filename in os.listdir(DIRECTORY_NAME):
        f = os.path.join(DIRECTORY_NAME, filename)
        if os.path.isfile(f):
            if "discover" in f:
                text = extract_text(f)
                parsed.extend(parse_discover(text))
            elif "chase" in f:
                text = extract_text(f)
                parsed.extend(parse_chase(text))
    return parsed


# Prompts the user to sort each purchase into a category
def sort_purchases(categories: dict[int, Category], purchases: list[Purchase]) -> None:
    print(f"Categories: {categories}")
    for i in range(len(purchases)):
        category_num = input(f"Enter category for '{purchases[i].description}': ")
        categories[category_num].amount += purchases[i].price  


categories = get_categories()
purchases = parse_statements()
sort_purchases(categories, purchases)
for category in categories.values():
    print(category)