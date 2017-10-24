TELEGRAM_API_TOKEN = '441081825:AAEIAEmMpgNcFf4axlgW0qEs30jXpxwsyro'

START_MSG = 'Здравствуйте! Отправьте фотографию своего документа для обработки:)'
HELP_MSG = 'это help msg'

ABBYY_CLOUD_OCR_USERNAME = 'kurpiyanovartem@yandex.ru'
ABBYY_CLOUD_OCR_PASSWORD = '123456789'
ABBYY_CLOUD_OCR_APPLICATION_PASSWORD = 'a2Bwh/rAbE61XTu6+OGT/Jr9'

NOT_DOCUMENT_ERROR = 'Эта фотография не является документом для распознавания. Если это действительно документ, то ' \
                     'перефотографируйте его!'

TITLE_MSG = 'Название документа: {}\n\n'

BACK_TO_DICT = 'Вернуться к списку слов /dict\n'
BACK_TO_ROOT = 'Вернуться к корневой вершине дерева /root\n'
BACK_TO_PARENT = 'Вернуться к родительской вершине /parent\n'
BACK_TO_MENU_MSG = 'В главное меню /menu\n'
NEW_DOCUMENT_MSG = 'Для загрузки нового документа нажмите /start\n'

FUNCTIONAL_MSG = 'Вывести весь документ /print\n' \
                 'Навигация по документу с помощью дерева /tree\n' \
                 'Словарь юридических терминов /dict\n' \
                 'Нужна юридическая помощь квалифицированного юриста? /real_lawyer\n' + NEW_DOCUMENT_MSG


GET_REAL_LAYER = 'Список доступных юристов на {}:\n' \
                 'Иванов Иван Иванович тел. 88005553535, м.Тверская\n' \
                 'Петров Петр Петрович тел. 89995002020, м.Тимирязевская\n\n' + BACK_TO_MENU_MSG  + NEW_DOCUMENT_MSG

WAIT_MSG = 'Идет обработка фотографии... Пожалуйста, подождите'

THATS_ALL_MSG = 'Это все фотографии? Если да, то нажмите  /yes, иначе, ' \
                'просто продолжите заливать фотографии\n' + NEW_DOCUMENT_MSG


def get_tree_msg(tree_array):
    if len(tree_array) > 0:
        msg = '\n'.join(list(map(lambda x: '/t_' + str(x[0]) + ' ' + (x[1]),
                                zip(range(len(tree_array)), tree_array))))
        msg += '\n'
    else:
        msg = ''
    # print('msg', msg)
    msg += BACK_TO_ROOT
    msg += BACK_TO_PARENT
    msg += BACK_TO_MENU_MSG
    msg += NEW_DOCUMENT_MSG
    # print('final =', msg)
    return msg

LIST_DICTIONARY_COMMANDS = ['/d_{}'.format(i) for i in range(1000)]
LIST_TREE_COMMANDS = ['/t_{}'.format(i) for i in range(1000)]


def get_dict_msg(keys_in_text):
    if len(keys_in_text) == 0:
        return 'Слов из словаря не найдено\n' + BACK_TO_MENU_MSG + NEW_DOCUMENT_MSG
    msg = '\n'.join(list(map(lambda x: '/d_' + str(x[0]) + ' ' + x[1], zip(range(len(keys_in_text)), keys_in_text))))
    msg += '\n'
    msg += BACK_TO_MENU_MSG
    msg += NEW_DOCUMENT_MSG
    return msg


def get_meaning_msg(word, meaning):
    msg = '*' + word.strip() + '* -- ' + meaning + '\n'
    msg += BACK_TO_DICT
    msg += BACK_TO_MENU_MSG
    msg += NEW_DOCUMENT_MSG
    return msg