import os

from web_crawler import WebCrawler

if __name__ == "__main__":
    months = [
        (2022, "january"), (2022, "february"), (2022, "march"), (2022, "april"), (2022, "may"), (2021, "june"), (2022, "july"),
        (2022, "august"), (2022, "september"), (2022, "october")]

    for year, month in months:
        path = f"wsj_{year}_{month}"

        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path)
            print(f"{path} is created!")
        start_day = 0
        start_order = 0
        web_crawler = WebCrawler(year, month, start_day, start_order)
        web_crawler.main_entry()
