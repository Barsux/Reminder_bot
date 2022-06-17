from dial import cli, get_default_markup
from dial.dialogs import Remind_Dialog, find_dial, reset_dial, dials_exist
from telebot import types



@cli.message_handler(commands= ['help'])
def help(message):
    cli.send_message(message.chat.id, "Я не знаю много команд:", reply_markup=get_default_markup())

@cli.message_handler(commands = ['reset'])
def reset(message):
    reset_dial(message.chat.id)


@cli.message_handler(content_types=['text'])
def message_handler(message):
    eval_again = True
    if message.text == "Добавить напоминание":
        dialog = find_dial(message.chat.id)
        if(not dialog):
            dialog = Remind_Dialog(message.chat.id)
        while eval_again:
            replies, reply_markup, eval_again = dialog.evaluate(message.text)
            for reply in replies:
                if reply:
                    cli.send_message(message.chat.id, reply, reply_markup=reply_markup if reply_markup else None)
    elif message.text == "Отмена":
        cli.send_message(message.chat.id, "Создание напоминания отменено", reply_markup=get_default_markup() )
        reset_dial(message.chat.id)
    elif dials_exist():
        dialog = find_dial(message.chat.id)
        while eval_again:
            replies, reply_markup, eval_again = dialog.evaluate(message.text)
            for reply in replies:
                if reply:
                    cli.send_message(message.chat.id, reply, reply_markup=reply_markup if reply_markup else None)
    else:
        cli.send_message(message.chat.id, "Хрен", reply_markup=get_default_markup())

cli.polling(none_stop=True, interval=0)