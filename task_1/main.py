from pymongo import MongoClient
from pymongo.server_api import ServerApi


client = MongoClient(
    "mongodb+srv://pigwowa:qwerty1234@cluster0.mz77bil.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.cat_book

def find_all():
    result = db.cats.find({})
    return result

def find_one(name: str):
    result = db.cats.find_one({"name": name})
    return result

def update_age(name: str, age: int):
    result = db.cats.update_one({"name": name}, {"$set": {"age": age}})
    return result

def update_features(name: str, var: str):
    result = db.cats.update_one({"name": name}, {"$push": {"features": var}})
    return result

def delete_cat(name: str):
    result = db.cats.delete_one({"name": name})
    return result

def delete_all():
    result = db.cats.delete_many({})
    return result

find = find_one("Bob")

if __name__ == '__main__':

    # Реалізуйте функцію для видалення всіх записів із колекції:
    refresh_db = delete_all()

    # Створіть базу даних відповідно до вимог:
    insert_data = db.cats.insert_many([
        {
            "name": "Lama",
            "age": 2,
            "features": ["neat", "does't let itself pet", "gray"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["neat", "lets itself pet", "white"],
        },
        {
            "name": "Alexa",
            "age": 3,
            "features": ["neat", "lets itself pet", "bronze"],
        },
        {
            "name": "Simon",
            "age": 7,
            "features": ["shits", "doesn't let itself pet", "ginger"],
        },
        {
            "name": "Markiza",
            "age": 19,
            "features": ["shits", "lets itself pet", "black"],
        },
    ])
    print(150 * "-")

    print(insert_data.inserted_ids)

    print(150 * "-")

    print("Реалізуйте функцію для виведення всіх записів із колекції:")
    list = find_all()
    for el in list:
        print(el)

    print(150 * "-")

    print("Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота:")
    print(find_one("Alexa"))

    print(150 * "-")

    print("Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям:")
    update_age("Simon", 10)
    print(find_one("Simon"))

    print(150 * "-")

    print("Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям:")
    update_features("Alexa", "curly")
    print(find_one("Alexa"))

    print(150 * "-")

    print("Реалізуйте функцію для видалення запису з колекції за ім'ям тварини:")
    delete_cat("Markiza")
    list = find_all()
    for el in list:
        print(el)








    

