# utf-8
import re
import datetime

def check_numbering(input_text):
    sentences_list = input_text.split("\n")
    count = 0
    for sentence in sentences_list:
        if re.search("\d.\d", sentence):
            count += 1
        if count > 3:
            return True
    return False


def get_title(text):
    upd_msg = list(map(lambda x: x.strip(), text.split('\n')))
    if '' in upd_msg:
        index = upd_msg.index('')
        dirt = ' '.join(upd_msg[0:index]).strip()
        reg = re.compile('[^a-zA-Z0-9а-яА-Я№()<>«»_ ]')
        ans = ' '.join(reg.sub('', dirt).split())
        return True, ans
    else:
        return False, ''


def get_date():
    months = dict(zip(range(1, 13),
                      ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
                       'Июля', 'Сентября', 'Октября', 'Ноября', 'Декабря']))
    date = datetime.date.today()
    date = str(date).split('-')
    date[1] = months[int(date[1])]
    return ' '.join(date[::-1])