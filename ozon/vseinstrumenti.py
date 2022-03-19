import datetime

from ozon.parsser_class import ParserVseinstrumenti


def main():
    HEADERS = {
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    catigoris = ['perforatory', 'akkumulyatornyj', 'dreli', 'kraskopulty', 'izmeritelnyj',
                 'instrument/feny_termopistolety', 'borozdodely_shtroborezy', 'shurupoverty', 'frezery',
                 'pily', 'rubanki', 'gravery', 'steplery', 'kompressory', 'svarochnoe-oborudovanie']
    CSV = f'Vseinstrumenti{datetime.date.today()}.csv'

    parser = ParserVseinstrumenti(HEADERS, catigoris, CSV)
    parser.parser()


if __name__ == '__main__':
    main()
