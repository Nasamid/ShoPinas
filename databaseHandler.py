from datetime import datetime, timedelta
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

def get_latest_daily_sales_table(connection):
    cursor = connection.cursor()

    try:
        # Fetch the names of all tables in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Filter tables that start with "daily_sales_" and extract the dates
        date_format = "%Y%m%d"
        table_dates = [
            datetime.strptime(table[0].replace("daily_sales_", ""), date_format).date()
            for table in tables
            if table[0].startswith("daily_sales_")
        ]

        # Find the latest date
        latest_date = max(table_dates, default=None)

        if latest_date:
            # Construct the latest daily_sales table name
            latest_table_name = f"daily_sales_{latest_date.strftime(date_format)}"
            return latest_table_name
        else:
            print("No daily_sales table found in the database.")
            return None

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error getting latest daily_sales table: {e}")
        return None

    finally:
        # Close the cursor
        cursor.close()

def add_daily_sale(connection, product_id, quantity, subtotal):
    cursor = connection.cursor()

    try:
        # Get the latest daily_sales table
        latest_table = get_latest_daily_sales_table(connection)

        if latest_table:
            # Insert a new row into the latest daily_sales table
            query = f"INSERT INTO `{latest_table}` (productID, quantity, subtotal) VALUES ({product_id}, {quantity}, {subtotal})"
            cursor.execute(query)

            # Commit the changes to the database
            connection.commit()
        else:
            print("No daily_sales table found for the latest date.")

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

from datetime import datetime, timedelta

def get_previous_latest_daily_sales_table(db_connection):
    cursor = db_connection.cursor()

    # Get all tables with the prefix "daily_sales_"
    cursor.execute("SHOW TABLES LIKE 'daily_sales_%'")
    all_tables = cursor.fetchall()

    # Check if there are at least two tables
    if len(all_tables) >= 2:
        # Extract dates from the table names
        dates = [int(table[0].split('_')[2]) for table in all_tables]

        # Sort the dates in descending order
        sorted_dates = sorted(dates, reverse=True)

        # Find the second-to-last date
        previous_latest_date = sorted_dates[1]

        # Construct the table name for the second-to-last date
        previous_latest_table_name = f"daily_sales_{previous_latest_date}"

        cursor.close()
        return previous_latest_table_name
    else:
        # If there are not enough tables, return None
        cursor.close()
        return None

def create_daily_sales_table(db_connection):
    # Get the current date
    current_date = datetime.now().strftime("%Y%m%d")

    # Check if the table for the current date exists
    table_exists_query = f"SHOW TABLES LIKE 'daily_sales_{current_date}'"
    cursor = db_connection.cursor()
    cursor.execute(table_exists_query)
    table_exists = cursor.fetchone()

    # If the table exists, increment the date and create a new table
    if table_exists:
        latest_table_query = "SELECT MAX(TABLE_NAME) FROM information_schema.tables WHERE TABLE_NAME LIKE 'daily_sales_%'"
        cursor.execute(latest_table_query)
        latest_table = cursor.fetchone()[0]

        if latest_table:
            latest_date_str = latest_table.split("_")[2]
            latest_date_obj = datetime.strptime(latest_date_str, "%Y%m%d")
            next_date_obj = latest_date_obj + timedelta(days=1)
            next_date = next_date_obj.strftime("%Y%m%d")
            table_name = f"daily_sales_{next_date}"

            print(table_name)

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
        else:
            print("Error getting latest table.")
            table_name = None
    else:
        print("Table doesn't exist")
        table_name = f"daily_sales_{current_date}"

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