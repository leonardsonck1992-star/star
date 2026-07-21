import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


main_url = "https://books.toscrape.com/"

response = requests.get(main_url, timeout=15)

soup = BeautifulSoup(
    response.content,
    "html.parser"
)

print(response.status_code)


category_section = soup.find(
    "div",
    class_="side_categories"
)

category_links = category_section.find_all("a")


for link in category_links[1:]:
    category_name = link.text.strip()

    category_url = urljoin(
        main_url,
        link["href"]
    )

    print("Starting category:", category_name)

    csv_file_name = (
        category_name
        .replace(" ", "_")
        .lower()
        + ".csv"
    )

    with open(
        csv_file_name,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "product_page_url",
            "upc",
            "book_title",
            "price_including_tax",
            "price_excluding_tax",
            "quantity_available",
            "product_description",
            "category",
            "review_rating",
            "image_url"
        ])

        current_page_url = category_url

        while current_page_url:
            print("Opening category page:", current_page_url)

            category_response = requests.get(
                current_page_url,
                timeout=15
            )

            category_soup = BeautifulSoup(
                category_response.content,
                "html.parser"
            )

            books = category_soup.find_all(
                "article",
                class_="product_pod"
            )

            for book in books:
                relative_url = (
                    book.find("h3")
                    .find("a")["href"]
                )

                product_page_url = urljoin(
                    current_page_url,
                    relative_url
                )

                print("Scraping:", product_page_url)

                book_response = requests.get(
                    product_page_url,
                    timeout=15
                )

                book_soup = BeautifulSoup(
                    book_response.content,
                    "html.parser"
                )

                book_title = (
                    book_soup.find("h1").text
                )

                upc = (
                    book_soup.find("table")
                    .find_all("td")[0]
                    .text
                )

                price_excluding_tax = (
                    book_soup.find("table")
                    .find_all("td")[2]
                    .text
                )

                price_including_tax = (
                    book_soup.find("table")
                    .find_all("td")[3]
                    .text
                )

                quantity_available = (
                    book_soup.find("table")
                    .find_all("td")[5]
                    .text
                )

                product_description = (
                    book_soup.find_all("p")[3]
                    .text
                )

                category = (
                    book_soup.find(
                        "ul",
                        class_="breadcrumb"
                    )
                    .find_all("a")[2]
                    .text
                )

                review_rating = (
                    book_soup.find(
                        "p",
                        class_="star-rating"
                    )["class"][1]
                )

                image_url = (
                    book_soup.find("img")["src"]
                )

                writer.writerow([
                    product_page_url,
                    upc,
                    book_title,
                    price_including_tax,
                    price_excluding_tax,
                    quantity_available,
                    product_description,
                    category,
                    review_rating,
                    image_url
                ])

            next_button = category_soup.find(
                "li",
                class_="next"
            )

            if next_button:
                next_page = (
                    next_button.find("a")["href"]
                )

                current_page_url = urljoin(
                    current_page_url,
                    next_page
                )

            else:
                current_page_url = None

    print(category_name, "CSV complete")