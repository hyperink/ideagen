import datetime
import csv
    
def prune(lst, blacklst):
    """
    Prune a list so it doesn't contain any words within a blacklist of
    stop words
    """
    return [word.lower() for word in lst if isinstance(word, basestring) and not word.lower() in blacklst]


def scoredtopics2csv(scoredtopics, desc="_default"):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d@%H:%M")
    spamWriter = csv.writer(open('data/' + current_time + desc + '.csv', 'wb'), delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamWriter.writerow(["topic_id", "score"])
    for ts in scoredtopics:
        spamWriter.writerow(ts)

