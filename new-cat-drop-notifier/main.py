from interfaces import OHSAdoptPage


def main():
    cat_adoption_page = OHSAdoptPage("cats")
    print(cat_adoption_page.all_animals)


if __name__ == '__main__':
    main()
