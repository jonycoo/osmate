import os
import logging
import bot_osm_edit
import ee_osmose
import osmose
from telegram import *
import telegram.error
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler, CallbackContext)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    TOKEN = os.environ['BOT_TOKEN']
except KeyError:
    logger.exception('no "BOT_TOKEN" token in environment variables.', 'Exit program')
    exit()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    help(update, context)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send me a location, I will give you some Issues near this location.',
                              'send /user <username> ,'
                              ' I will give you some Issues where this user was the last editor')
    
    
def loc_issue(update: Update, context):
    loc: Location = update.message.location
    if not loc:
        loc = Location(float(context.args[1]), float(context.args[0]))
    try:
        issues = osmose.get_issues_loc(loc.latitude, loc.longitude, 500)
        pager = osmose.Pager(issues, 10)
        context.user_data['list'] = pager
        send_issues(update.message.bot, update.effective_chat.id, pager)
        logger.info('executed loc_issue()')
    except ee_osmose.NoneFoundError as err:
        error(update, context, err)


def user_issue(update: Update, context: CallbackContext):
    logger.debug('Entering: user_issue')
    user = context.args[0]
    try:
        issues = osmose.get_issues_user(user)
        logger.debug(issues)
        pager = osmose.Pager(issues, 10)
        context.user_data['list'] = pager
        send_issues(update.message.bot, update.effective_chat.id, pager)
        logger.info('executed user_issue()')
    except ee_osmose.NoneFoundError as err:
        error(update, context, err)


def send_issue(bot: Bot, chat_id: str, issue: osmose.Issue):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Location', callback_data=issue.id),
                                      InlineKeyboardButton('Welt', callback_data='edit')]])

    bot.send_message(chat_id, issue.__str__(), reply_markup=keyboard)


def prep_keyboard(num):
    """prepares an InlineKeyboardMarkup with as much buttons as elements but max 5 each row"""
    keyboard = [[InlineKeyboardButton("Prev", callback_data='prev'),
                 InlineKeyboardButton("Next", callback_data='next')]]
    buttons = []
    for i in range(num):
        buttons.append(InlineKeyboardButton(str(i+1), callback_data=str(i)))
    for i in range(0, len(buttons), 5):
        keyboard.append(buttons[i:i + 5])
    logger.debug('keyboard prepared')
    return InlineKeyboardMarkup(keyboard)


def send_issues(bot: Bot, chat_id, pager):
    logger.debug('Entering: send_issues')
    pager.next()
    keyboard = prep_keyboard(len(pager.curr()))
    msg = osmose.Pager.to_msg(pager.curr())
    logger.debug('send list of issues')
    bot.send_message(chat_id, msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def next_iss(query, context: CallbackContext):
    logger.debug('in next_iss')
    nx_pg = context.user_data['list'].next()
    iss_msg = osmose.Pager.to_msg(nx_pg)
    query.edit_message_text(iss_msg, reply_markup=prep_keyboard(len(nx_pg)), parse_mode=ParseMode.HTML)


def prev_iss(query: CallbackQuery, context: CallbackContext):
    logger.debug('in prev_iss')
    pv_pg = context.user_data['list'].prev()
    iss_msg = osmose.Pager.to_msg(pv_pg)
    query.edit_message_text(iss_msg, reply_markup=prep_keyboard(len(pv_pg)), parse_mode=ParseMode.HTML)


def more_iss(query: CallbackQuery, context: CallbackContext):
    """reply more details of the Issue"""
    logger.debug('in more_iss')
    lst = context.user_data['list'].curr()
    iss = osmose.get_issue(lst[int(query.data)].id)
    context.user_data['det_iss'] = iss
    del context.user_data['list']
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Location', callback_data='loc'),
                                      InlineKeyboardButton('Description', url=iss.desc_url())], [InlineKeyboardButton('Edit', callback_data='edit')]])
    query.edit_message_text(str(iss), reply_markup=keyboard, parse_mode=ParseMode.HTML)


def iss_loc(query, context):
    issue = context.user_data['det_iss']
    link = InlineKeyboardMarkup([[InlineKeyboardButton('OSM', issue.osm_url())]])
    query.edit_message_text(query.message.text, parse_mode=ParseMode.HTML)
    query.bot.sendLocation(query.message.chat_id, issue.lat, issue.lon,
                           reply_to_message_id=query.inline_message_id,
                           reply_markup=link)


def button(update: Update, context):
    query: CallbackQuery = update.callback_query

    if query.data == 'next':
        next_iss(query, context)
        query.answer()
    elif query.data == 'prev':
        prev_iss(query, context)
        query.answer()
    elif query.data == 'loc':
        iss_loc(query, context)
        query.answer()
    elif query.data.startswith('edit'):
        return
    else:
        more_iss(query, context)
        query.answer()

    print(query.data)


def error(update, context, err: Exception):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    bot: Bot = update.message.bot
    bot.send_message(update.effective_chat.id, err.args[0])


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    editor = bot_osm_edit.ElemEditor()
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help), 1)
    dp.add_handler(CommandHandler('user', user_issue), 1)
    dp.add_handler(CallbackQueryHandler(button), 1)
    dp.add_handler(CommandHandler("loc", loc_issue), 1)
    dp.add_handler(editor.get_conversation(), 0)

    # on non-command i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    try:
        # Start the Bot
        updater.start_polling()
    except telegram.error.NetworkError:
        logger.error('could not connect to Telegram Server')


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
