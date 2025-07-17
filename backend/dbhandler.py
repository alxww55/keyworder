import os
from .requester import Requester
import sqlite3

class DatabaseHandler(Requester):
    def __init__(self):
        super().__init__()
        try:
            os.mkdir("data")
        except FileExistsError:
            pass
        self.conn = sqlite3.connect("data/application.db")
        self.cur = self.conn.cursor()
        self.path = "data/application.db"

    def create_db(self):
        """
        Checks whether the SQLite database file exists at the specified path.

        If the database file exists, returns True. Otherwise, raises a FileNotFoundError.
        This function can be used as a basic check before interacting with the database.

        Returns
        -------
        bool
            True if the database file exists, False if it does not or an error occurred.
        """
        try:
            if os.path.isfile(self.path):
                return True
            else:
                raise FileNotFoundError("Database missing and/or cannot be created")
        except Exception as e:
            print(f"Database error: {e}")
            return False
        
    def create_table(self):
        """
        Creates the `Products` table in the SQLite database if it does not already exist.

        The table contains fields such as ID, SKU, image URL, multilingual names,
        keywords, multilingual descriptions, status, and price.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the SQL execution fails (e.g., due to a syntax or connection error).
        """
        try:
            self.cur.execute("CREATE TABLE IF NOT EXISTS Products(ID PRIMARY KEY UNIQUE, SKU, Image_URL, Name_RU, Name_UA, Keywords, Description_RU, Description_UA, Status, Price)")
        except Exception as e:
            print(e)

    def update_product(self, product: dict):
        """
        Inserts or updates a product in the `Products` table based on the product's ID.

        If the product already exists (matched by ID), it updates the record with the latest
        values including name, SKU, images, descriptions, status, and calculated price
        (adjusted for any applicable discount). If it doesn't exist, a new row is inserted.

        Parameters
        ----------
        product : dict
            A dictionary representing a single product, including pricing, multilingual data,
            discount type and value, and all necessary metadata fields.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the database operation fails (e.g., due to invalid field or connection error).
        """
        try:
            if product["discount"] != None:
                match product["discount"]["type"]:
                    case "percent":
                        price = product["price"] * (1 - product["discount"]["value"] / 100)
                    case "amount":
                        price = product["price"] - product["discount"]["value"]
            else:
                price = product["price"]

            self.cur.execute("""
                INSERT INTO Products (ID, SKU, Image_URL, Name_RU, Name_UA, Keywords, Description_RU, Description_UA, Status, Price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ID) DO UPDATE SET
                    SKU = excluded.SKU,
                    Image_URL = excluded.Image_URL,
                    Name_RU = excluded.Name_RU,
                    Name_UA = excluded.Name_UA,
                    Keywords = excluded.Keywords,
                    Description_RU = excluded.Description_RU,
                    Description_UA = excluded.Description_UA,
                    Status = excluded.Status,
                    Price = excluded.Price
                """,
                (product["id"], product["sku"], product["main_image"], product["name_multilang"]["ru"], product["name_multilang"]["uk"], product["keywords"], product["description_multilang"]["ru"], product["description_multilang"]["uk"], product["status"], price))
        except Exception as e:
            print(f"Error updating product {product['id']}: {e}")

    def load_data_into_db(self):
        """
        Loads product data from the remote API into the local SQLite database.

        Retrieves product data using the `get_request()` method inherited from the `Requester` class.
        For each product, calls `update_product()` to insert or update the corresponding database entry.
        After processing all products, commits the transaction to save changes.

        Returns
        -------
        None

        Raises
        ------
        sqlite3.DatabaseError
            If the response is empty or invalid.
        Exception
            If an error occurs during processing or database operations.
        """
        try:
            self.json_data = super().get_request()
            if self.json_data is not None:
                for product in self.json_data["products"]:
                    self.update_product(product)
                self.conn.commit()
            else:
                raise sqlite3.DatabaseError("Error while inserting data!")
        except Exception as e:
            print(e)