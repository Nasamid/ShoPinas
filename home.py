import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, ttk, Frame
from databaseHandler import connect_to_database, create_table, insert_data, query_and_print_data, close_connection, query_and_get_data
import importlib

# MySQL connection details
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_password = '123'
mysql_database = 'shopinas_database'

# Connect to the MySQL database
db_connection = connect_to_database(mysql_host, mysql_user, mysql_password, mysql_database)

window = Tk()

window.geometry("750x525+400+150")
window.configure(bg = "#F0F0F0")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\danil\OneDrive\Desktop\JR\ShoPinas\New folder\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

canvas = Canvas(
    window,
    bg = "#F0F0F0",
    height = 525,
    width = 750,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    188.0,
    270.0,
    image=image_image_1
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    -5.0,
    -25.0,
    785.0,
    50.0,
    fill="#FFFFFF",
    outline="#000000")

canvas.create_text(
    177.93130493164062,
    13.0,
    anchor="nw",
    text="SALES TRACKER",
    fill="#424550",
    font=("Josefin Sans", 20 * -1)
)

canvas.create_text(
    11.48614501953125,
    -7,
    anchor="nw",
    text="Sho",
    fill="#FF0000",
    font=("Josefin Sans", 36 * -1)
)

canvas.create_text(
    97.26156616210938,
    -7,
    anchor="nw",
    text="i",
    fill="#F3BF07",
    font=("Josefin Sans", 36 * -1)
)

canvas.create_text(
    73.77542114257812,
    -7,
    anchor="nw",
    text="P nas",
    fill="#032FA1",
    font=("Josefin Sans", 36 * -1)
)

canvas.create_rectangle(
    57.0,
    335.0,
    309.0,
    496.0,
    fill="#FFFFFF",
    outline="")

#MONTHLY SALES RECT
canvas.create_rectangle(
    57.0,
    335.0,
    309.0,
    496.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    21.0,
    111.0,
    345.0,
    294.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    21.0,
    111.0,
    345.0,
    294.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    426.0,
    105.0,
    722.0,
    468.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    426.0,
    105.0,
    722.0,
    468.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    27.0,
    87.0,
    anchor="nw",
    text="MONTHLY SALES",
    fill="#000000",
    font=("Josefin Sans", 13 * -1)
)

canvas.create_text(
    638.0,
    83.0,
    anchor="nw",
    text="DAILY SALES",
    fill="#000000",
    font=("Josefin Sans", 13 * -1)
)

canvas.create_text(
    57.0,
    310.0,
    anchor="nw",
    text="CHOOSE A MONTH",
    fill="#000000",
    font=("Josefin Sans", 13 * -1)
)

canvas.create_rectangle(
    426.0,
    480.0,
    529.0,
    505.0,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=426.0,
    y=480.0,
    width=103.0,
    height=29.0
)

canvas.create_rectangle(
    566.0,
    480.0,
    640.0,
    505.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    648.0,
    480.0,
    722.0,
    505.0,
    fill="#FFFFFF",
    outline="")

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=648.0,
    y=480.0,
    width=76.0,
    height=28.0
)

# Function to display daily sales in a Tkinter table
def display_daily_sales():
    # Specify the columns you want, including the product name
    query = 'SELECT products.name, daily_sales.quantity, daily_sales.subtotal FROM daily_sales JOIN products ON daily_sales.productID = products.productID'
    data = query_and_get_data(db_connection, query)

    if not data:
        print("No data found.")
        return

    # Create a Frame inside the Canvas to hold the Treeview
    tree_frame = Frame(window, bg="#FFFFFF", bd=0, highlightthickness=0)
    tree_frame.place(x=426.0, y=105.0, width=722.0 - 426.0, height=468.0 - 105.0)
    # Create a Treeview widget
    tree = ttk.Treeview(tree_frame, columns=["Product", "Quantity", "Subtotal (Php)"], show='headings')
    
    # Add columns to the Treeview
    for col in ["Product", "Quantity", "Subtotal (Php)"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)  # Adjust the width as needed

    # Add data to the Treeview
    for row in data:
        tree.insert('', 'end', values=row)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    # Pack the Treeview and scrollbar
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

# Function to display monthly sales in a Tkinter table
def display_monthly_sales():
    query = 'SELECT month, total FROM monthly_sales'  # Specify the columns you want
    data = query_and_get_data(db_connection, query)

    if not data:
        print("No data found.")
        return

    # Create a Frame inside the Canvas to hold the Treeview for monthly_sales
    monthly_sales_frame = Frame(window, bg="#FFFFFF", bd=0, highlightthickness=0)
    monthly_sales_frame.place(x=57.0, y=335.0, width=309.0 - 57.0, height=496.0 - 335.0)

    # Create a Treeview widget
    tree = ttk.Treeview(monthly_sales_frame, show='headings')

    # Add columns to the Treeview
    columns_to_display = ["Month", "Total"]
    tree["columns"] = tuple(columns_to_display)

    for column in columns_to_display:
        tree.heading(column, text=column)
        tree.column(column, width=100)  # Adjust the width as needed

    # Add data to the Treeview
    for row in data:
        tree.insert('', 'end', values=row)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(monthly_sales_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Pack the Treeview and scrollbar
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

def open_add_sales_window():
    add_sales_window = Toplevel(window)
    add_sales_window.geometry("607x345")
    add_sales_window.configure(bg="#FFFFFF")
    
    # Import addSales.py module
    import addSales

    # Call the necessary functions from addSales.py
    addSales.display_daily_sales()
    # You can call other functions if needed

    
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command = open_add_sales_window,
    relief="flat"
)

button_2.place(
    x=566.0,
    y=480.0,
    width=85.0,
    height=29.0
)

def on_mouse_move(event):
    x, y = event.x, event.y
    display_daily_sales()


#window.bind("<Motion>", on_mouse_move)
# Automatically display the daily sales table upon window startup
display_daily_sales()
display_monthly_sales()

window.resizable(False, False)
window.mainloop()
