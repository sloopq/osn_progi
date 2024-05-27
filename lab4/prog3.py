from schema import factory
from schema import Region
from sqlalchemy.orm.exc import NoResultFound

# Создаём сессию для взаимодействия с базой данных
session = factory()

# Список регионов, которые мы будем добавлять
regions = ["Africa", "Asia", "Europe",
           "Pacific", "North America",
           "South America"]

# Добавляем каждый регион в сессию, если его ещё нет в базе данных
for reg in regions:
    try:
        # Проверяем, существует ли регион в базе данных
        existing_region = session.query(Region).filter_by(region_name=reg).one()
        print(f"Регион {reg} уже существует в базе данных.")
    except NoResultFound:
        # Если регион не найден, добавляем его
        r = Region()
        r.region_name = reg
        session.add(r)
        print(f"Регион {reg} добавлен в базу данных.")

# Сохраняем изменения в базе данных
session.commit()
