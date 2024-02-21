import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="kroll"
)

cursor = db_connection.cursor()

def display_all_products():
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    for product in products:
        print(product)

def display_all_customers():
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    for customer in customers:
        print(customer)

def sales_per_category():
    cursor.execute("SELECT p.category, COUNT(*) as sales_count "
                   "FROM Product p "
                   "JOIN Orders o ON p.id = o.product_id "
                   "GROUP BY p.category;")
    sales = cursor.fetchall()
    for sale in sales:
        print(sale)

def top_customers_by_spending():
    cursor.execute("SELECT c.first_name, c.last_name, SUM(o.product_total_sum) as total_spent "
                   "FROM Customer c "
                   "JOIN Orders o ON c.id = o.client_id "
                   "GROUP BY c.id "
                   "ORDER BY total_spent DESC "
                   "LIMIT 10;")
    top_customers = cursor.fetchall()
    for customer in top_customers:
        print(customer)

def average_price_per_category():
    cursor.execute("SELECT category, AVG(price) as average_price "
                   "FROM Product "
                   "GROUP BY category;")
    average_prices = cursor.fetchall()
    for avg_price in average_prices:
        print(avg_price)

def most_popular_product():
    cursor.execute("SELECT p.product_name, SUM(o.product) as total_sold "
                   "FROM Product p "
                   "JOIN Orders o ON p.id = o.product_id "
                   "GROUP BY p.id "
                   "ORDER BY total_sold DESC "
                   "LIMIT 1;")
    most_popular = cursor.fetchall()
    for popular in most_popular:
        print(popular)

def available_products():
    cursor.execute("SELECT * FROM Product "
                   "WHERE availability = 1 "
                   "AND id NOT IN (SELECT DISTINCT product_id FROM Orders);")
    available = cursor.fetchall()
    for product in available:
        print(product)

def add_product():
    product_name = input("Введіть назву продукту: ")
    product_description = input("Введіть опис продукту: ")
    price = float(input("Введіть ціну продукту: "))
    category = input("Введіть категорію продукту: ")
    availability = int(input("Введіть доступність продукту (1 - доступний, 0 - недоступний): "))
    supplier_id = int(input("Введіть ID постачальника: "))
    
    cursor.execute("INSERT INTO Product (product_name, product_description, price, category, availability, supplier_id) "
                   "VALUES (%s, %s, %s, %s, %s, %s)",
                   (product_name, product_description, price, category, availability, supplier_id))
    db_connection.commit()
    print("Продукт успішно додано!")

while True:
    print("\nМеню:")
    print("1. Вивести всі продукти")
    print("2. Вивести всіх замовників")
    print("3. Кількість продажів для кожної категорії товарів")
    print("4. Клієнти з найвищою сумою замовлень")
    print("5. Середня ціна товарів для кожної категорії")
    print("6. Додати продукт")
    print("7. Вихід")

    choice = input("Виберіть пункт меню: ")

    if choice == "1":
        display_all_products()
    elif choice == "2":
        display_all_customers()
    elif choice == "3":
        sales_per_category()
    elif choice == "4":
        top_customers_by_spending()
    elif choice == "5":
        average_price_per_category()
    elif choice == "6":
        add_product()
    elif choice == "7":
        print("Дякую за використання програми. До побачення!")
        break
    else:
        print("Невірний вибір. Спробуйте ще раз.")

db_connection.close()
