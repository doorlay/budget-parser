import os
import pymupdf
import csv

DIRECTORY_NAME = "statements"

CAPITALONE_MONTHS = {
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec"
}

class Purchase:
    def __init__(self, description, price, is_venmo=False):
        self.description = description
        if is_venmo:
            self.price = extract_price_venmo(price)
        else: 
            self.price = extract_price(price)

    def __str__(self):
        return f"Description: {self.description}\nPrice: {self.price}"


# Represents a budget category, customized by the user
class Category:
    def __init__(self, name):
        self.name = name
        self.amount = 0

    def __repl__(self):
        return f"{self.name}: ${round(self.amount, 2)}"

    def __str__(self):
        return f"{self.name}: ${round(self.amount, 2)}"


# Given a string, determines if it's a date (in the context of bank statement formatting)
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


# Given a string, determines if it's a date (in CapitalOne's formatting)
def is_date_capitalone(date_string: str) -> bool:
    split_date_string = date_string.strip().split(" ")
    if len(split_date_string) != 2:
        return False
    if split_date_string[0].lower() in CAPITALONE_MONTHS:
        try:
            int(split_date_string[1])
        except ValueError:
            return False
        return True
    else:
        return False


# Extract a purchase's price from the string containing it
def extract_price(price_line: str) -> float:
    try:
        return float(price_line.replace("+", "").replace("$", "").replace(",", "").replace(" ", ""))
    except ValueError:
        print(f"Cannot convert {price_line} to float.")


# Extract a purchase's price from the string containing it, but for Venmo (since we can have positive values)
def extract_price_venmo(price_line: str) -> float:
    try:
        stripped_price = price_line.replace("$", "").replace(",", "").replace(" ", "")
        if "-" in stripped_price:
            return float(stripped_price.replace("-", ""))
        elif "+" in stripped_price:
            return 0 - float(stripped_price.replace("+", ""))
    except ValueError:
        print(f"Cannot convert {price_line} to float.")


# Given the extracted text of a Capital One statement, create a list of purchase objects
def parse_capitalone(text) -> list[Purchase]:
    lines = text[2].split("Transactions \nTrans Date \nPost Date \nDescription \nAmount")[1].split("\n")[1:]
    purchases = []
    for index, line in enumerate(lines):
        # If the current line is a date, it is potentially the beginning of a new row
        if is_date_capitalone(line):
            # Beginning of new line has two sequential dates. Confirm that to prevent duplicates
            if not is_date_capitalone(lines[index + 1]):
                continue 
            offset = 2
            purchase_description = ""
            purchase_amount = "" 
            # Iterate through the remaining columns in the document to grab all purchase data
            while True:
                description = lines[index + offset]
                if "$" in description:
                    purchase_amount = description[1:].split(" ")[0] 
                    purchases.append(Purchase(purchase_description, purchase_amount))
                    break
                purchase_description += description
                offset += 1
    return purchases


# Given a CSV filename for a Venmo statement, create a list of Purchase objects
def parse_venmo(file_name: str) -> list[Purchase]:
    purchases = [] 
    with open(file_name, "r") as csv_obj:
        csv_file = csv.reader(csv_obj)
        for index, row in enumerate(csv_file):
            # Ignore transfers from your Venmo account to your bank
            if row[3] == "Standard Transfer":
                continue
            # Ignore empty lines
            if len(row[1]) == 0:
                continue
            # Ignore the metadata in the statement
            if index < 4:
                continue
            if row[3] == "Charge":
                description = f"{row[6]} charged {row[7]} for {row[5]}"
            if row[3] == "Payment":
                description = f"{row[6]} paid {row[7]} for {row[5]}"
            purchases.append(Purchase(description, row[8], is_venmo=True))
    return purchases


# Given the extracted text of a Chase statement, create a list of Purchase objects
def parse_chase(text) -> list[Purchase]:
    lines = text[2].split("$ Amount")[1].split("\n")[4:]
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
                # If this line is for a card payment, skip it 
                if "Payments and Credits" in description:
                    break
                # If this line is for a statement credit redemeption, skip it
                if "AUTOMATIC STATEMENT CREDIT" in description:
                    break
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
    while True:
        new_category_name = input("Input category name, or 0 when done: ")
        if new_category_name in categories:
            print("Category name in use, try again.")
            continue
        if new_category_name == "0":
            break
        else:
            categories[new_category_name] = Category(new_category_name)
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
            elif "venmo" in f:
                parsed.extend(parse_venmo(f))
            elif "capitalone" in f:
                text = extract_text(f)
                parsed.extend(parse_capitalone(text))
    return parsed


# Prompts the user to sort each purchase into a category
def sort_purchases(categories: dict[str, Category], purchases: list[Purchase]) -> None:
    for i in range(len(purchases)):
        # Keep looping until user enters a valid category number
        while True:
            category_name = input(f"Enter category for '{purchases[i].description}': ")
            try:
                categories[category_name].amount += purchases[i].price 
                break 
            except KeyError:
                print(f"Invalid category name entered, please try again.")


categories = get_categories()
purchases = parse_statements()
# Print out each category so the user knows their options for sorting
for category in categories.keys():
    print(category)
sort_purchases(categories, purchases)
# After all sorting is complete, print out each category with their cumulative amounts
for category in categories.values():
    print(category)