from requests import get
from bs4 import BeautifulSoup


def main():
    params = {"type": "cats"}
    response = get("https://www.oregonhumane.org/adopt/", params)
    soup = BeautifulSoup(response.text, 'html.parser')
    cat_results = soup.find_all("div", {"class": "result-item"})
    cat_names = [cat_result["data-ohssb-name"] for cat_result in cat_results]
    print(cat_names)


if __name__ == '__main__':
    main()
