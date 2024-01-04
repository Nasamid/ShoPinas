from datetime import datetime
import os
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, ttk, Frame
from matplotlib.backend_bases import NavigationToolbar2
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from databaseHandler import connect_to_database, create_daily_sales_table, fetch_monthly_sales_data, get_previous_latest_daily_sales_table, query_and_get_data
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# MySQL connection details
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_password = '123'
mysql_database = 'shopinas_database'

# Connect to the MySQL database
db_connection = connect_to_database(mysql_host, mysql_user, mysql_password, mysql_database)

tree = None

def relative_to_assets(path: str) -> Path:
    output_path = Path(__file__).parent
    assets_path = output_path / Path(r"C:\Users\danil\OneDrive\Desktop\JR\ShoPinas\New folder\build\assets\frame0")
    return assets_path / Path(path)

def display_daily_sales(data):
    global tree
    # Create a Frame inside the Canvas to hold the Tre]eview
    tree_frame = Frame(window, bg="#FFFFFF", bd=0, highlightthickness=0)
    tree_frame.place(
        x=532.5, 
        y=131.25,
        width=902.5 - 532.5,
        height=585.0 - 131.25
    )
    # Create a Treeview widget
    tree = ttk.Treeview(tree_frame, columns=["Product", "Quantity", "Subtotal (Php)"], show='headings')
    
    # Add columns to the Treeview
    tree.heading(0, text="Product")
    tree.column(0, width=160) 

    tree.heading(1, text="Quantity", anchor = "center")
    tree.column(1, width=35, anchor = "center") 

    tree.heading(2, text="Subtotal (Php)", anchor = "center")
    tree.column(2, width=50, anchor = "center")  

    # Add data to the Treeview
    for row in data:
        tree.insert('', 'end', values=row)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    # Pack the Treeview and scrollbar
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    tree.yview_moveto(1.0)

def update_monthly_sales(db_connection, monthID):
    cursor = db_connection.cursor()

    # Get the current date
    current_date = datetime.now().strftime("%Y%m%d")

    table_name = get_previous_latest_daily_sales_table(db_connection)

    # Fetch the subtotal values from the current daily_sales table
    cursor.execute(f"SELECT subtotal FROM {table_name}")
    subtotal_values = [row[0] for row in cursor.fetchall()]

    # Calculate the total for the current month
    total_for_month = sum(subtotal_values)

    # Update the corresponding month in the monthly_sales table
    update_query = f"""
    UPDATE monthly_sales
    SET total = total + {total_for_month}
    WHERE msID = '{monthID}'
    """
    cursor.execute(update_query)

    db_connection.commit()
    cursor.close()

def save_button_clicked():
    # Create a new daily_sales table
    table_name = create_daily_sales_table(db_connection)

    # Update the monthly_sales table
    current_month = 1  # Change this to the actual current month
    update_monthly_sales(db_connection, current_month)

    daily_sales_data = query_and_get_data(db_connection, f'SELECT products.name, `{table_name}`.quantity, `{table_name}`.subtotal FROM `{table_name}` JOIN products ON `{table_name}`.productID = products.productID')
    display_daily_sales(daily_sales_data)

    messagebox.showinfo("Save", f"Data saved to Database and monthly sales updated.")

    db_connection.close()

def open_addSales_and_destroy_window():
    window.destroy()
    os.system('python addSales.py')

def get_latest_daily_sales_table(db_connection):
    cursor = db_connection.cursor()

    # Get the latest daily_sales table with a date later than today
    current_date = datetime.now().strftime("%Y%m%d")
    cursor.execute(f"SHOW TABLES LIKE 'daily_sales_%'")
    tables = cursor.fetchall()

    # Find the latest table with a date later than today
    latest_table = None
    for table in tables:
        table_date_str = table[0].replace("daily_sales_", "")
        table_date = datetime.strptime(table_date_str, "%Y%m%d")
        if table_date > datetime.now():
            if latest_table is None or table_date > latest_table:
                latest_table = table_date

    cursor.close()
    return f"daily_sales_{latest_table.strftime('%Y%m%d')}" if latest_table else None

def main():
    global window
    window = Tk()

    window.geometry("938x656+500+200")
    window.configure(bg="#F0F0F0")

    canvas = Canvas(
        window,
        bg="#F0F0F0",
        height=656,
        width=938,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        225.0,
        337.5,
        image=image_image_1
    )

    canvas.create_rectangle(
        0.0, 
        -31.25,
        1356.25,
        62.5,
        fill="#FFFFFF", 
        outline="#000000"
    )

    canvas.create_text(
        222.41413157050078,
        16.25,
        anchor="nw",
        text="SALES TRACKER",
        fill="#424550",
        font=("Josefin Sans", 20 * -1)
    )

    canvas.create_text(
        14.3576806640625,
        -8.75, 
        anchor="nw",
        text="Sho",
        fill="#FF0000",  
        font=("Josefin Sans", 36 * -1)
    )

    canvas.create_text(
        121.57469577651172,
        -8.75,
        anchor="nw",
        text="i",
        fill="#F3BF07",
        font=("Josefin Sans", 36 * -1)  
    )

    canvas.create_text(
        92.21892768554688,
        -8.75,
        anchor="nw",
        text="P nas",
        fill="#032FA1",
        font=("Josefin Sans", 36 * -1)
    )

    canvas.create_rectangle(
        171.25,
        418.75,
        386.25, 
        620.0,
        fill="#FFFFFF",
        outline="")

    #MONTHLY SALES RECT
    canvas.create_rectangle(
        200.25,
        418.75,
        386.25,
        620.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        156.25,
        138.75,  
        431.25,
        367.5,
        fill="#FFFFFF",
        outline="")
    
    #GRAPH RECT
    canvas.create_rectangle(
        26.25,
        138.75,
        431.25,
        367.5,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        532.5,
        131.25,
        902.5,
        585.0,
        fill="#FFFFFF", 
        outline="")

    canvas.create_rectangle(
        532.5,
        131.25,
        902.5,
        585.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        287.5,
        108.75, 
        anchor="nw",
        text="MONTHLY SALES",
        fill="#000000",
        font=("Josefin Sans", 13 * -1)
    )

    canvas.create_text(
        797.5,
        103.75,
        anchor="nw",
        text="DAILY SALES",
        fill="#000000", 
        font=("Josefin Sans", 13 * -1)
    )

    canvas.create_text(
        285.0, 
        375.5,
        anchor="nw",
        text="CHOOSE A MONTH",
        fill="#000000",
        font=("Josefin Sans", 13 * -1)
    )

    canvas.create_rectangle(
        532.5,
        600.0,
        661.25,
        631.25, 
        fill="#FFFFFF",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=save_button_clicked,
        relief="flat"
    )
    button_1.place(
        x=532.5, 
        y=600.0,
        width=128.75, 
        height=36.25
    )

    canvas.create_rectangle(
        707.5,
        600.0,
        800.0,
        631.25,
        fill="#FFFFFF",
        outline="")
    
    canvas.create_rectangle(
        810.0,
        600.0,
        902.5,
        631.25,
        fill="#FFFFFF",
        outline="")

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(  
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=delete_selected_row,
        relief="flat"
    )
    button_3.place(
        x=810.0,
        y=600.0, 
        width=95.0,
        height=35.0  
    )
    
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    
    button_2 = Button(
        image=button_image_2, 
        borderwidth=0,
        highlightthickness=0,
        command=open_addSales_and_destroy_window,
        relief="flat" 
    )

    button_2.place(
        x=707.5,
        y=600.0,
        width=106.25,
        height=36.25
    )

    # Create a Frame inside the Canvas to hold the Treeview for monthly_sales
    monthly_sales_frame = Frame(window, bg="#FFFFFF", bd=0, highlightthickness=0)
    monthly_sales_frame.place(
        x=100.25,
        y=400.75, 
        width=315,
        height=220
    )
    data = query_and_get_data(db_connection, 'SELECT month, total FROM monthly_sales')

    # Create a Treeview widget
    tree = ttk.Treeview(monthly_sales_frame, show='headings')

    # Add columns to the Treeview
    columns_to_display = ["Month", "Total"]
    tree["columns"] = tuple(columns_to_display)

    for column in columns_to_display:
        tree.heading(column, text=column)
        tree.column(column, width=100, anchor= "center")  # Adjust the width as needed

    # Add data to the Treeview
    for row in data:
        tree.insert('', 'end', values=row)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(monthly_sales_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Pack the Treeview and scrollbar
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    selected_item = tree.selection()
    selected_row_values = tree.item(selected_item)['values']

    # Create a Matplotlib line graph
    graph_frame = Frame(window, bg="#FFFFFF", bd=0, highlightthickness=0)
    graph_frame.place(
        x=26.25,
        y=78.75,
        width=470, 
        height=367.5 - 78.75
    )

    months = [row[0] for row in data]
    totals = [row[1] for row in data]

    # Adjust the figure size as needed
    figsize = (18, 10)  # You can experiment with different sizes
    plt.figure(figsize=figsize, dpi=50)
    plt.plot(months, totals, marker='o', color='b')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.title('M O N T H L Y   S A L E S')
    plt.grid(True)

    canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side='top', fill='both')
    plt.gcf().set_size_inches(6,4)

    current_date = datetime.now().strftime("%Y%m%d")

    # Get the latest daily_sales table
    latest_table = get_latest_daily_sales_table(db_connection)

    if latest_table:
        daily_sales_data = query_and_get_data(db_connection, f'SELECT products.name, `{latest_table}`.quantity, `{latest_table}`.subtotal FROM `{latest_table}` JOIN products ON `{latest_table}`.productID = products.productID')
        display_daily_sales(daily_sales_data)

    window.resizable(False, False)
    window.mainloop()

def delete_selected_row():
    global tree  # Access the global variable
    if tree:
        selected_item = tree.selection()
        if selected_item:
            # Get the selected row values
            selected_row_values = tree.item(selected_item)['values']

            # Extract relevant data
            product_name = selected_row_values[0]
            quantity = selected_row_values[1]

            current_table = get_latest_daily_sales_table(db_connection)

            # Delete the row from the daily_sales_{current_date} table
            delete_query = f"DELETE FROM {current_table} WHERE productID = (SELECT productID FROM products WHERE name = '{product_name}') AND quantity = {quantity}"
            cursor = db_connection.cursor()
            cursor.execute(delete_query)
            db_connection.commit()
            cursor.close()

            # Delete the selected item from the Treeview
            tree.delete(selected_item)
        else:
            messagebox.showinfo("Delete Error", "Please select a row to delete.")
    else:
        messagebox.showinfo("Tree Error", "Tree is not initialized.")

if __name__ == "__main__":
    main()
