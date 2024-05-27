from schema import factory
from schema import Country


session = factory()

c = session.query(Country).where(Country.country_name == "Zambia").first()

print(c.regions)
print("Region name:", c.regions.region_name)
