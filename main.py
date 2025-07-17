from dotenv import load_dotenv
from backend.dbhandler import DatabaseHandler
  
load_dotenv()

db = DatabaseHandler()
db.create_db()
db.create_table()
db.load_data_into_db()


























































# class ProductDB(Requester):
#     def __init__(self):
#         super().__init__()
#         self.products = []

#     def pr(self):
#         try:
#             self.json_data = super().get_request()
#             if self.json_data != None:
#                 for product in self.json_data["products"]:
#                     product = {"id": product["id"], "name": product["name"], "sku": product["sku"],"keywords": product["keywords"], "price": product["price"], "discount": product["discount"], "currency": product["currency"]}
#                     self.products.append(product)
#                     return self.products
#             else:
#                 raise Exception
#         except Exception as e:
#             print(e)

# load_dotenv()
# pr = ProductDB()


# re = Requester()
# re.post_request(json_body=[
#         {
#             "id": 2679771757,
#             "name": "Тестирую перевод",
#             "keywords": "Тестовые слова, продвижение, программирование"
#         }
#     ]
# )

# prod = pr.pr()
# print(f"ID: {prod[0]["id"]}")
# print(f"Название: {prod[0]["name"]}")
# print(f"SKU: {prod[0]["sku"]}")
# print(f"Ключевые слова: {prod[0]["keywords"]}")
# print(f"Цена: {prod[0]["price"]} {prod[0]["currency"]}")

# pu = re.translate_product(json_body={
#         "product_id": "2679771757",
#         "lang": "uk",
#         "name": "Тестую переклад",
#         "keywords": "Тестові слова, просування, програмування"
#     }
# )