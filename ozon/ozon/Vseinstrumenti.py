import datetime

from parsser_class import ParserVseinstrumenti


def main():
    HOST = 'https://spb.vseinstrumenti.ru/instrument/'
    pages = int(input('Укажите кол-во страниц'))
    parser = ParserVseinstrumenti(HOST, pages)
    parser.parser()


if __name__ == '__main__':
    main()
