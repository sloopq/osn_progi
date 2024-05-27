from schema import factory, Country

session = factory()

# Список стран для добавления или обновления
countries = [
    {"country_name": "Russia", "region_id": 3},
    {"country_name": "Zambia", "region_id": 1},
    # добавьте другие страны здесь
]

for country in countries:
    # Проверка на существование записи
    existing_country = session.query(Country).filter_by(country_name=country["country_name"]).first()
    if existing_country:
        # Обновление существующей записи
        existing_country.region_id = country["region_id"]
        print(f"Updated country {country['country_name']}.")
    else:
        # Создание новой записи
        new_country = Country(**country)
        session.add(new_country)

try:
    session.commit()
except Exception as e:
    session.rollback()
    print(f"Ошибка: {e}")
finally:
    session.close()
