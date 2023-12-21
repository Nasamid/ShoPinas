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

def add_daily_sale(connection, product_id, quantity, subtotal):
    """Add a new row to the daily_sales table."""
    cursor = connection.cursor()

    try:
        # Insert a new row into the daily_sales table
        query = f"INSERT INTO daily_sales (productID, quantity, subtotal) VALUES ({product_id}, {quantity}, {subtotal})"
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error adding daily sale: {e}")

    finally:
        # Close the cursor
        cursor.close()

def close_connection(connection):
    """Close the MySQL database connection."""
    connection.close()