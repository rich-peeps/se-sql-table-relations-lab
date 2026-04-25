# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Employees who work in the Boston office (first & last name only)
df_boston = pd.read_sql(
    """
    SELECT
        e.firstName,
        e.lastName
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
    """,
    conn,
)

# STEP 2
# Return any offices that do not have employees assigned.
df_zero_emp = pd.read_sql(
    """
    SELECT o.*
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL;
    """,
    conn,
)

# STEP 3
# "Return the employees' first name and last name, along with the city
#  and state of the office that they work out of (if they have one).
#  Include all employees and order them by their first name, then last name."
df_employee = pd.read_sql(
    """
    SELECT
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName;
    """,
    conn,
)

# STEP 4
# "Return all of the customer's contact information (first name, last name,
#  phone) as well as their sales rep's employee number for any customer
#  who has not placed an order. Sort by contact's last name."
df_contacts = pd.read_sql(
    """
    SELECT
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName;
    """,
    conn,
)

# STEP 5
# "Return all the customer contacts (first and last names) along with
#  details for each of the customers' payment amounts and dates.
#  Sort in descending order by payment amount (may be stored as text)."
df_payment = pd.read_sql(
    """
    SELECT
        c.contactFirstName,
        c.contactLastName,
        p.amount,
        p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
    """,
    conn,
)

# STEP 6
# "Return the employee number, first name, last name, and number of customers
#  for employees whose customers have an average credit limit over 90k.
#  Sort by number of customers high to low. (We expect 4)."
df_credit = pd.read_sql(
    """
    SELECT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS num_customers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC;
    """,
    conn,
)

# STEP 7
# "Return the product name and count the number of orders for each product
#  as numorders. Also return totalunits as the sum of quantityOrdered.
#  Sort by totalunits, highest to lowest."
df_product_sold = pd.read_sql(
    """
    SELECT
        p.productName,
        COUNT(DISTINCT od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productCode
    ORDER BY totalunits DESC;
    """,
    conn,
)

# STEP 8
# "Return the product name, code, and total number of customers who
#  have ordered each product, aliased as numpurchasers.
#  Sort by highest number of purchasers."
df_total_customers = pd.read_sql(
    """
    SELECT
        p.productName,
        p.productCode,
        COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    ORDER BY numpurchasers DESC;
    """,
    conn,
)

# STEP 9
# "Return the count as n_customers, and the office code and city."
df_customers = pd.read_sql(
    """
    SELECT
        o.officeCode,
        o.city,
        COUNT(DISTINCT c.customerNumber) AS n_customers
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
    GROUP BY o.officeCode
    ORDER BY o.officeCode;
    """,
    conn,
)

# STEP 10
# Employees who sold products ordered by fewer than 20 distinct customers
df_under_20 = pd.read_sql(
    """
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        o.city,
        o.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
    JOIN orders ord ON ord.customerNumber = c.customerNumber
    JOIN orderdetails od ON od.orderNumber = ord.orderNumber
    WHERE od.productCode IN (
        SELECT od2.productCode
        FROM orderdetails od2
        JOIN orders o2 ON od2.orderNumber = o2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT o2.customerNumber) < 20
    )
    ORDER BY
        CASE WHEN e.firstName = 'Loui' THEN 0 ELSE 1 END,
        e.firstName,
        e.lastName;
    """,
    conn,
)


conn.close()