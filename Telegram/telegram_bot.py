import telebot
import logging
import config
import os
from Parse_templates import tree_contract as our_tree
from Termin_dictionary import get_weird_words as our_dict

import Utils.utils as utils
import time

bot = telebot.TeleBot(config.TELEGRAM_API_TOKEN)

logger = logging.getLogger(__name__)
handler = logging.FileHandler("my_logger.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

texts = {}
titles = {}
dicts = {}
trees = {}
roots = {}


@bot.message_handler(commands=["yes"])
def yes(message):
    msg = bool(titles[message.chat.id]) * config.TITLE_MSG.format(titles[message.chat.id])  + config.FUNCTIONAL_MSG
    bot.send_message(message.chat.id, msg)


# если мы отправляем фото
@bot.message_handler(content_types=["photo"])
def img2text(message):
    # print('msg', message.photo[0])
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file = bot.get_file(fileID)
    print('file.file_path =', file.file_path)
    file_name = file.file_path.split('/')[-1]
    link = 'https://api.telegram.org/file/bot' + config.TELEGRAM_API_TOKEN + '/' + file.file_path
    os.system('wget ' + link)
    os.system('mv ' + file_name + ' ../OCR/Saved_photos/')
    resp_img = ' ../OCR/Saved_photos/' + file_name
    resp_text = ' ../OCR/Saved_texts/' + file_name.split('.')[0] + '.txt'
    print('bash  ../OCR/ocr_sdk.sh ' + resp_img + resp_text + ' -l Russian -f txt')
    bot.send_message(message.chat.id, config.WAIT_MSG)
    os.system('bash  ../OCR/ocr_sdk.sh ' + resp_img + resp_text + ' -l Russian -f txt')
    with open(resp_text.strip()) as f:
        our_text = f.read()

    if len(our_text) < 100:
        bot.send_message(message.chat.id, config.NOT_DOCUMENT_ERROR)

    if message.chat.id in texts.keys():
        texts[message.chat.id] += " "
        texts[message.chat.id] += our_text
    else:
        texts[message.chat.id] = our_text

    have_title, title = utils.get_title(our_text)
    if message.chat.id in titles.keys():
        pass
    else:
        titles[message.chat.id] = title

    bot.send_message(message.chat.id, config.THATS_ALL_MSG)


@bot.message_handler(commands=["tree", "root"])
def get_tree(message):
    try:
        root = our_tree.build_tree(texts[message.chat.id])
        trees[message.chat.id] = root
        roots[message.chat.id] = root

        childs_values = root.get_childs_data()
        # print('childs', childs_values)
        msg = config.get_tree_msg(childs_values)
        bot.send_message(message.chat.id, msg)
    except Exception:
        pass


@bot.message_handler(func=lambda message: message.text in config.LIST_TREE_COMMANDS)
def print_children(message):
    safe_vertex = trees[message.chat.id]
    try:
        num = int(message.text.split('_')[-1])
        vertex = trees[message.chat.id]
        vertex = vertex.to_child(num)
        trees[message.chat.id] = vertex
        print('vertex', vertex)
        if vertex is not None:
            childs_values = vertex.get_childs_data()
            if len(childs_values) == 0:
                childs_values = [vertex.data]
            print('childs', childs_values)
            msg = config.get_tree_msg(childs_values)
            bot.send_message(message.chat.id, msg)
        else:
            msg = config.get_tree_msg([])
            bot.send_message(message.chat.id, msg)

    except Exception:
        trees[message.chat.id] = safe_vertex


@bot.message_handler(commands=["parent"])
def print_parent(message):
    safe_vertex = trees[message.chat.id]
    try:
        vertex = trees[message.chat.id]
        if vertex.parent is not None:
            vertex = vertex.parent
        if vertex is not None:
            childs_values = vertex.get_childs_data()
            msg = config.get_tree_msg(childs_values)
            bot.send_message(message.chat.id, msg)
        else:
            msg = config.get_tree_msg([])
            bot.send_message(message.chat.id, msg)
    except Exception:
        trees[message.chat.id] = safe_vertex


@bot.message_handler(func=lambda message: message.text in config.LIST_DICTIONARY_COMMANDS)
def print_meaning_word(message):
    try:
        num = int(message.text.split('_')[-1])
        word = sorted(dicts[message.chat.id].keys())[num]
        meaning = (dicts[message.chat.id])[word]
        msg = config.get_meaning_msg(word, meaning)
        bot.send_message(message.chat.id, msg)
    except Exception:
        pass


@bot.message_handler(commands=["dict"])
def get_dict(message):
    try:
        dict_in_text = dict(our_dict.find_law_words(texts[message.chat.id]))
        dicts[message.chat.id] = dict_in_text
        keys_in_text = sorted(dict_in_text.keys())
        msg = config.get_dict_msg(keys_in_text)
        bot.send_message(message.chat.id, msg)
    except Exception:
        pass


@bot.message_handler(func=lambda message: message.text in config.LIST_DICTIONARY_COMMANDS)
def print_meaning_word(message):
    try:
        num = int(message.text.split('_')[-1])
        word = sorted(dicts[message.chat.id].keys())[num]
        meaning = (dicts[message.chat.id])[word]
        msg = config.get_meaning_msg(word, meaning)
        bot.send_message(message.chat.id, msg)
    except Exception:
        pass


@bot.message_handler(commands=["real_lawyer"])
def get_real_lawyer(message):
    bot.send_message(message.chat.id, config.GET_REAL_LAYER.format(utils.get_date()))


@bot.message_handler(commands=["menu"])
def get_menu(message):
    bot.send_message(message.chat.id, config.FUNCTIONAL_MSG.format(titles[message.chat.id]))


@bot.message_handler(commands=["print"])
def get_menu(message):
    bot.send_message(message.chat.id, config.FUNCTIONAL_MSG.format(titles[message.chat.id]))
    i = 0
    while i * 4000 < len(texts[message.chat.id]):
        right = min((i + 1) * 4000 + 1, len(texts[message.chat.id]))
        bot.send_message(message.chat.id, (texts[message.chat.id])[i * 4000:right])
        i += 1
        time.sleep(3)

@bot.message_handler(commands=["start"])
def handle_start(message):
    texts[message.chat.id] = ''
    titles[message.chat.id] = ''
    bot.send_message(message.chat.id, config.START_MSG)
    # info_log(message.chat.id, config.LOG_START)


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, config.HELP_MSG)
    # info_log(message.chat.id, config.LOG_HELP)

if __name__ == '__main__':
    bot.polling(none_stop=True)
