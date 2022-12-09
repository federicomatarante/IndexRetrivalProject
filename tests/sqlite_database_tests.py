from unittest import TestCase

from src.database.sqlite_database import TableSchema, SQLiteView


class Test(TestCase):

    def test_schema_1(self):
        schema = TableSchema(name='Review',
                             attributes={
                                 'text': 'TEXT',
                                 'product': 'TEXT NOT NULL'},
                             slope=['FOREIGN KEY(product) REFERENCES Product(title)',
                                    'PRIMARY KEY(text,product)'])
        print(schema)
        print(schema.creationQuery)

    def test_schema_2(self):
        schema = TableSchema(name='Product',
                             attributes={
                                 'title': 'TEXT PRIMARY KEY',
                                 'description': 'TEXT NULLABLE'})
        print(schema)
        print(schema.creationQuery)

    def test_schema_3(self):
        schema = TableSchema(name='Bread')
        print(schema)
        print(schema.creationQuery)

    def test_connection(self):
        view = SQLiteView(file='test.sqlite', schemas=[])
        print(view.isConnected())
        print("Connecting...")
        view.connect()
        print(view.isConnected())
        print("Disconnecting...")
        view.disconnect()
        print(view.isConnected())

    def test_tables(self):
        reviews = TableSchema(name='Review',
                              attributes={
                                  'text': 'TEXT',
                                  'product': 'TEXT NOT NULL'},
                              slope=['FOREIGN KEY(product) REFERENCES Product(title)',
                                     'PRIMARY KEY(text,product)'])
        products = TableSchema(name='Product',
                               attributes={
                                   'title': 'TEXT PRIMARY KEY',
                                   'description': 'TEXT NULLABLE'})
        view = SQLiteView(file='test.sqlite', schemas=[products, reviews])
        view.connect()
        print(f"DoTablesExist: {view.doTablesExist()}")
        view.createTables()
        print("Creating tables...")
        print(f"DoTablesExist: {view.doTablesExist()}")
        print("Deleting tables...")
        view.dropTables("Review", "Product")
        print(f"DoTablesExist: {view.doTablesExist()}")

    def test_insert(self):
        reviews = TableSchema(name='Review',
                              attributes={
                                  'text': 'TEXT',
                                  'product': 'TEXT NOT NULL'},
                              slope=['FOREIGN KEY(product) REFERENCES Product(title)',
                                     'PRIMARY KEY(text,product)'])
        products = TableSchema(name='Product',
                               attributes={
                                   'title': 'TEXT PRIMARY KEY',
                                   'description': 'TEXT NULLABLE'})
        view = SQLiteView(file='test.sqlite', schemas=[products, reviews])
        view.connect()
        if not view.doTablesExist():
            view.createTables()
        print("Selecting product...")
        result = view.select(table='Product', attributes=['title', 'description'], where="title == 'Iphone'")
        print(f"Result: {result}")
        print("Inserting product...")
        view.insertOne(table='Product', item={'title': 'Iphone', 'description': 'Non lo so'})
        result = view.select(table='Product', attributes=['title', 'description'], where="title == 'Iphone'")
        print(f"Result: {result}")
        print("Deleting product...")
        view.delete(table='Product', where=f"title == 'Iphone'")
        result = view.select(table='Product', attributes=['title', 'description'], where="title == 'Iphone'")
        print(f"Result: {result}")
        view.disconnect()

    def test_insert_2(self):
        reviews = TableSchema(name='Review',
                              attributes={
                                  'text': 'TEXT',
                                  'product': 'TEXT NOT NULL'},
                              slope=['FOREIGN KEY(product) REFERENCES Product(title)',
                                     'PRIMARY KEY(text,product)'])
        products = TableSchema(name='Product',
                               attributes={
                                   'title': 'TEXT PRIMARY KEY',
                                   'description': 'TEXT NULLABLE'})
        view = SQLiteView(file='test.sqlite', schemas=[products, reviews])
        view.connect()
        if not view.doTablesExist():
            view.createTables()
        print("Selecting product...")
        result = view.select(table='Product', attributes=['title', 'description'], where="title == 'Android'")
        print(f"Result: {result}")
        print("Inserting product...")
        view.insertOne(table='Product', item={'title': 'Android'})
        result = view.select(table='Product', attributes=['title', 'description'], where="title == 'Android'")
        print(f"Result: {result}")
        print("Deleting product...")
        view.delete(table='Product', where=f"title == 'Android'")
        result = view.select(table='Product', attributes=['title', 'description'], where="title == 'Android'")
        print(f"Result: {result}")
        view.disconnect()



