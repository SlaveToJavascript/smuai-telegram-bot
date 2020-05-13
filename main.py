from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import telegram
import requests
import datetime

called_articles = []


def get_article(api, called_articles):
    contents = requests.get(api).json()
    articles_array = [[x, "Unread"] for x in contents['articles'] if x not in called_articles]
    return articles_array


def send_article(title, url, channel_monitoring_id, target_id, bot):
    # json format
    # top level objects: status, totalResults, articles(array)
    # articles objects: source(array), author, title, description, url, urlToImage, publishedAt, content
    # source objects: id, name
    content = "*" + title + "*\n\nRead More: [Source](" + url + ")"
    m = bot.send_message(chat_id=channel_monitoring_id, text=content, parse_mode=telegram.ParseMode.MARKDOWN)
    bot.forward_message(chat_id=target_id, from_chat_id=channel_monitoring_id, message_id=m['message_id'])


def news_push(bot, job):
    bot.send_message(chat_id=-1001461874044, text="Pushing...", parse_mode=telegram.ParseMode.MARKDOWN)
    current_dt = datetime.datetime.now()
    articles = get_article('https://newsapi.org/v2/everything?q="Artificial Intelligence"&sources=time,ars-technica,fortune,reuters,bbc-news,wired,next-big-future,techcrunch,techradar,recode&from=' + current_dt.strftime("%Y-%m-%d") + '&to=' + current_dt.strftime("%Y-%m-%d") + '&apiKey=87a00708b6ba4febaa222c75998a9fed', called_articles)
    # articles = get_article('https://newsapi.org/v2/everything?q=%22Artificial%20Intelligence%22&sources=bbc-news&from=2019-02-14&to=2019-02-15&apiKey=87a00708b6ba4febaa222c75998a9fed',
    #                       called_articles) ignore this, for debugging only

    for article in articles:
        if article[1] == "Unread":
            article[1] = "Read"
            called_articles.append(article[0])
            send_article(article[0]['title'], article[0]['url'], '-1001461874044', '-1001381637659', bot)
            #'-1001461874044' smu ai news bot monitoring
            #'-1001381637659' smu ai chat
        else:
            pass

def refresh(bot, job):
    #clear read articles
    global called_articles
    called_articles = []


def start_services(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Starting news services for the day!')


    # job_queue.run_repeating(news_push, 10) ignore this, for debugging only to test every 10s if bot is alive

    #1800s = 30mins
    #push every 30 mins
    job_queue.run_repeating(news_push, 1800)
    # job_queue.run_repeating(refresh, 10) ignore this, for debugging only to test every 10s if bot is alive
    #172800s = 2days
    #clear every 2 days
    job_queue.run_repeating(refresh, 172800)




def main():
    current_dt = datetime.datetime.now()
    print(current_dt.strftime("%Y-%m-%d"))
    updater = Updater('703281172:AAGCAZ5C7DNcGc3jZ1AkgOvCpFLG2ZgNHOg')
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx SMUAI NEWS BOT API
    # updater = Updater('-1461874044_864054736242426387') ignore this, for debugging only
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler('test', test)) ignore this
    dp.add_handler(CommandHandler('start_services', start_services, pass_job_queue=True))
    # dp.add_handler(CommandHandler('news_push', news_push)) ignore this, for debugging only
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
