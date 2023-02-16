from src.docsmanager import DocsDatabase
from src.index import ProductsIndex


def createIndex(index: ProductsIndex, directory: str):
    """
    Creates the index from the database.
    """
    if not index.exists():
        index.create()
    view = index.open()
    database = DocsDatabase(directory)
    print("Retreiving reviews...")
    reviews = database.getDocs()
    print("Retreived!")
    print(reviews)

    print("Adding to the index...")
    view.add(reviews)
    print("Added!")
    index.close()


def run():
    createIndex(ProductsIndex("indexdir"), 'Docs')


"""
The file is used to create the index from the database.
"""
if __name__ == '__main__':
    run()
