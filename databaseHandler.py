from datetime import datetime
import mysql.connector

def connect_to_database(host, user, password, database):
    """Connect to the MySQL database."""
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection

def create_table(connection, table_name, columns):
    """Create a table in the MySQL database."""
    cursor = connection.cursor()
    columns_definition = ', '.join(columns)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")
    connection.commit()

def insert_data(connection, table_name, data):
    """Insert data into the specified table in the MySQL database."""
    cursor = connection.cursor()
    placeholders = ', '.join(['%s' for _ in data])
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
    connection.commit()

def query_and_print_data(connection, query):
    """Execute a SELECT query and print the results from the MySQL database."""
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Print column names
    column_names = [description[0] for description in cursor.description]
    print("\t".join(column_names))

    # Print data
    for row in rows:
        print("\t".join(str(value) for value in row))

def query_and_get_data(connection, query):
    """Execute a SELECT query and return the results from the MySQL database."""
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

from datetime import datetime

def add_daily_sale(connection, product_id, quantity, subtotal):
    """Add a new row to the daily_sales table with the current date."""
    cursor = connection.cursor()

    try:
        # Get the current date in the format YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")

        # Construct the table name
        table_name = f"daily_sales_{current_date}"

        # Insert a new row into the dynamically named daily_sales table
        query = f"INSERT INTO {table_name} (productID, quantity, subtotal) VALUES ({product_id}, {quantity}, {subtotal})"
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error adding daily sale: {e}")

    finally:
        # Close the cursor
        cursor.close()

def fetch_monthly_sales_data(connection):
    """Fetch monthly sales data from the database."""
    cursor = connection.cursor()

    try:
        # Assuming your monthly_sales table has columns 'month' and 'total'
        query = "SELECT month, total FROM monthly_sales"
        cursor.execute(query)

        # Fetch all rows from the result
        monthly_sales_data = cursor.fetchall()

        return monthly_sales_data

    except Exception as e:
        print(f"Error fetching monthly sales data: {e}")
        return None

    finally:
        cursor.close()

def create_daily_sales_table(db_connection):
    # Create a new table with the current date as the name
    current_date = datetime.now().strftime("%Y%m%d")
    table_name = f"daily_sales_{current_date}"
    
    cursor = db_connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        salesID INT NOT NULL AUTO_INCREMENT, 
        productID INT,
        quantity INT,
        subtotal FLOAT,
        PRIMARY KEY (salesID),
        FOREIGN KEY (productID) REFERENCES products(productID)
    )
    """
    cursor.execute(create_table_query)

    db_connection.commit()
    cursor.close()

    return table_name

def close_connection(connection):
    """Close the MySQL database connection."""
    connection.close()