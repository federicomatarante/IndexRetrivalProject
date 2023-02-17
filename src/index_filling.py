from docsmanager import DocsDatabase
from index import ProductsIndex
from CollectDocument import create_path


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
    n,Doc = create_path()
    print(Doc)
    createIndex(ProductsIndex("indexdir"), Doc)


"""
The file is used to create the index from the database.
"""
if __name__ == '__main__':
    run()
