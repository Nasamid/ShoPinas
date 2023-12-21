import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from tkinter import StringVar
from databaseHandler import connect_to_database, query_and_get_data, close_connection, add_daily_sale
from home import display_daily_sales
#from home import display_daily_sales

# Connect to the MySQL database
db_connection = connect_to_database("127.0.0.1", "root", "123", "shopinas_database")

window = Tk()
window.geometry("607x345")
window.configure(bg = "#FFFFFF")

# Assuming you have a function to fetch product details based on the product ID
def fetch_product_details(product_id):
    query = f"SELECT name, price FROM products WHERE productID = {product_id}"
    result = query_and_get_data(db_connection, query)
    return result

def fetch_product_details_by_name(product_name):
    query = f"SELECT productID, price FROM products WHERE name = '{product_name}'"
    result = query_and_get_data(db_connection, query)
    return result


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\danil\OneDrive\Desktop\JR\ShoPinas\New folder (2)\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 345,
    width = 607,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    120.0,
    241.0,
    image=image_image_1
)

canvas.create_text(
    67.0,
    85.0,
    anchor="nw",
    text="PRODUCT ID",
    fill="#000000",
    font=("Josefin Sans", 12 * -1)
)

canvas.create_text(
    361.0,
    85.0,
    anchor="nw",
    text="PRODUCT NAME",
    fill="#000000",
    font=("Josefin Sans", 12 * -1)
)

canvas.create_text(
    212.0,
    140.0,
    anchor="nw",
    text="PRICE (Php)",
    fill="#000000",
    font=("Josefin Sans", 12 * -1)
)

canvas.create_text(
    212.0,
    202.0,
    anchor="nw",
    text="QUANTITY",
    fill="#000000",
    font=("Josefin Sans", 12 * -1)
)

canvas.create_rectangle(
    -5.0,
    -5.0,
    607.0,
    63.0,
    fill="#FFFFFF",
    outline="#000000")

canvas.create_text(
    15.0,
    5.0,
    anchor="nw",
    text="ADD A SALE",
    fill="#000000",
    font=("Josefin Sans", 32 * -1)
)

#PRODUCT ID
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    159.0,
    123.0,
    image=entry_image_1
)
entry_var_1 = StringVar()
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=5,
    textvariable=entry_var_1
)
entry_1.place(
    x=67.0,
    y=104.0,
    width=184.0,
    height=30.0
)

#QUANTITY
entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    304.0,
    247.0,
    image=entry_image_3
)
entry_var_3 = StringVar()
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=5,
    textvariable=entry_var_3
)
entry_3.place(
    x=212.0,
    y=228.0,
    width=184.0,
    height=36.0
)

# PRODUCT NAME
entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    453.0,
    123.0,
    image=entry_image_4
)
entry_var_4 = StringVar()
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=5,
    textvariable=entry_var_4
)
entry_4.place(
    x=361.0,
    y=104.0,
    width=184.0,
    height=36.0
)

#PRICE
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    304.0,
    185.0,
    image=entry_image_2
)

entry_var_2 = StringVar()
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=5,
    textvariable=entry_var_2
    
)
entry_2.place(
    x=212.0,
    y=166.0,
    width=184.0,
    height=36.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=5,
    command=lambda: window.destroy(),
    relief="flat"
)
button_1.place(
    x=314.0,
    y=304.0,
    width=97.0,
    height=32.0
)

# ... (your previous imports and functions)

def add_sale_to_daily_sales():
    # Get the values from entry_1 and entry_3
    product_id = entry_var_1.get()
    quantity = entry_var_3.get()

    try:
        # Try to convert quantity to an integer
        quantity = int(quantity)

        # Fetch product details from the database based on the product ID
        product_details = fetch_product_details(product_id)

        if product_details:
            # Calculate subtotal by multiplying price with quantity
            subtotal = product_details[0][1] * quantity

            # Add a row to the daily_sales table
            add_daily_sale(db_connection, product_id, quantity, subtotal)

            # Show a success message
            messagebox.showinfo("Success", "Sale added successfully.")
            window.destroy()

            # If you want to update the main window, call the function to refresh the data
            #display_daily_sales()

        else:
            # Product does not exist, show an error message
            messagebox.showerror("Product Not Found", f"Product with ID {product_id} does not exist.")
    except ValueError:
        # Invalid input (not an integer), you may handle this differently based on your needs
        messagebox.showerror("Invalid Quantity", "Please enter a valid quantity.")


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))

button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=5,
    command=lambda: add_sale_to_daily_sales(),
    relief="flat"
)
button_2.place(
    x=196.0,
    y=304.0,
    width=97.0,
    height=32.0
)

def increment_quantity():
    current_quantity = entry_var_3.get()

    try:
        if not current_quantity:
            # If entry_3 is empty, set it to 1
            entry_var_3.set(1)
        else:
            # Try to convert the current quantity to an integer
            current_quantity = int(current_quantity)
            
            # Increment the quantity by 1
            current_quantity += 1

            # Update entry_3 with the new quantity
            entry_var_3.set(current_quantity)
    except ValueError:
        # Invalid input (not an integer), you may handle this differently based on your needs
        entry_var_3.set("")  # Clear entry_3
        messagebox.showerror("Invalid Quantity", "Please enter a valid quantity.")

def decrement_quantity():
    current_quantity = entry_var_3.get()

    try:
        # Try to convert the current quantity to an integer
        current_quantity = int(current_quantity)
        
        # Decrement the quantity by 1, but ensure it doesn't go below 0
        current_quantity = max(0, current_quantity - 1)

        # Update entry_3 with the new quantity
        entry_var_3.set(current_quantity)
    except ValueError:
        # Invalid input (not an integer), you may handle this differently based on your needs
        entry_var_3.set("")  # Clear entry_3
        messagebox.showerror("Invalid Quantity", "Please enter a valid quantity.")

#ADD QUANTITY BUTTON
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=5,
    command=lambda: increment_quantity(),
    relief="flat"
)
button_3.place(
    x=325.0,
    y=270.0,
    width=31.0,
    height=24.0
)

#SUBTRACT 1 FROM QUANTITY
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=5,
    command=lambda: decrement_quantity(),
    relief="flat"
)
button_4.place(
    x=365.0,
    y=270.0,
    width=31.0,
    height=24.0
)

def on_entry_change(*args):
    # Get the content of entry_1
    product_id = entry_var_1.get()

    # Check if the product_id is not empty
    if not product_id:
        # Clear entry_2 and entry_4 if the field is empty
        entry_var_2.set("")
        entry_var_4.set("")
        return

    try:
        # Try to convert the input to an integer
        product_id = int(product_id)
        
        # Fetch product details from the database
        product_details = fetch_product_details(product_id)

        if product_details:
            # Product exists, update entry_4 with product name and entry_2 with price
            entry_var_4.set(product_details[0][0])  # Assuming the product name is in the first column
            entry_var_2.set(product_details[0][1])  # Assuming the price is in the second column
        else:
            # Product does not exist, show an error message
            messagebox.showerror("Product Not Found", f"Product with ID {product_id} does not exist.")
    except ValueError:
        # Invalid input (not an integer), you may handle this differently based on your needs
        entry_var_4.set("")  # Clear entry_4
        entry_var_2.set("")  # Clear entry_2
        messagebox.showerror("Invalid Input", "Please enter a valid product ID.")

def on_entry_4_enter(event):
    # Get the content of entry_4
    product_name = entry_var_4.get()

    # Check if the product_name is not empty
    if not product_name:
        # Clear entry_1, entry_2, and entry_4 if the field is empty
        entry_var_1.set("")
        entry_var_2.set("")
        entry_var_4.set("")
        return

    # Fetch product details from the database based on product name
    product_details = fetch_product_details_by_name(product_name)

    if product_details:
        # Product exists, update entry_1, entry_2, and entry_4
        entry_var_1.set(product_details[0][0])  # Assuming the product ID is in the first column
        entry_var_2.set(product_details[0][1])  # Assuming the price is in the second column
    else:
        # Product does not exist, show an error message
        messagebox.showerror("Product Not Found", f"Product with name '{product_name}' does not exist.")


# Bind the function to the Entry widget
entry_var_1.trace_add("write", on_entry_change)

# Bind the function to the <Return> event for entry_4
entry_4.bind("<Return>", on_entry_4_enter)

window.resizable(False, False)
window.mainloop()
