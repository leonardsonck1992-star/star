import csv
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
category_url = "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
response = requests.get(category_url)
soup = BeautifulSoup(response.content, 'html.parser')

books = soup.find_all("article", class_= "product_pod")
print(len(books))
product_page_urls = []
for book in books:
    relative_url = book.find("h3").find("a")["href"]
    product_page_url = urljoin(category_url,
 relative_url)
    product_page_urls.append(product_page_url)

print(len(product_page_urls))

with open("poetry_books.csv", "w", newline= "",
          encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow([
        "product_page_url",
        "upc",
        "book_title",
        "price_including_tax",
        "price_excluding_tax",
        "quanity_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ])
    for index, product_page_url in enumerate(product_page_urls, start=1):
        print(f"scraping book {index} of {len(product_page_urls)}")
        response = requests.get(product_page_url)
        book_soup = BeautifulSoup(response.content, "html.parser")
        book_title = book_soup.find("h1").text
        upc = book_soup.find("table").find_all("td")[0].text
        price_excluding_tax = book_soup.find("table").find_all("td")[2].text
        price_including_tax = book_soup.find("table").find_all("td")[3].text
        quantity_available = book_soup.find("table").find_all("td")[5].text
        product_description = book_soup.find_all("p")[3].text
        category = book_soup.find("ul", class_="breadcrumb").find_all("a")[2].text
        review_rating = book_soup.find("p", class_ ="star-rating")["class"][1]
        image_url = book_soup.find("img")["src"]
    
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
