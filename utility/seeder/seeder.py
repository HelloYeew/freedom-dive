import json
import os

from mirror.models import Country


def seed_country():
    """
    Seed osu's country data to Country table, will trying to update if the country already exist.
    Data source is in data/osu_countries.json.
    More info on data see info.md in data folder.
    """
    print("Seeding country table")
    with open(os.path.join(os.path.dirname(__file__), "data", "osu_countries.json"), "r") as file:
        print(f"Reading osu_countries.json file from {os.path.join(os.path.dirname(__file__), 'data', 'osu_countries.json')}")
        countries = json.load(file)
        for country in countries:
            print(f"Seed country {country['name']}")
            try:
                Country.objects.create(
                    acronym=country["acronym"],
                    name=country["name"],
                    display=True if country["display"] == 1 else False
                )
            except Exception as e:
                print(f"Error while seeding country {country['name']} with error : {e}, trying to update")
                Country.objects.filter(acronym=country["acronym"]).update(
                    name=country["name"],
                    display=True if country["display"] == 1 else False
                )
