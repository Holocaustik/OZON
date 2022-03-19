from parsser_class import ParserOzon


def main():
    brands = {'hammer': '-26303172/',
              'stavr': '-26303509/',
              'wester': '-27762156/',
              'tesla': '-100085446/',
              'kolner': '-31279645/',
              'patriot': '-100171486/',
              'zubr': '-26303502/'}
    main_divs = ['ii9 ', 'ji']
    name_class = 'hy9'
    price_class = 'ui-n9'
    review_class = 'vc6'
    rat_class = 'ui-ab8'
    sales_class = 'z9h'
    pages = int(1)
    parser = ParserOzon(main_divs, name_class, price_class, review_class, rat_class, sales_class, brands, pages)
    #result = parser.passer()
    #parser.save_result(result)
    parser.get_divs()


if __name__ == '__main__':
    main()
