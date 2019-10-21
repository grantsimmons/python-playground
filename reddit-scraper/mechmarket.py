import feedparser
import smtplib, ssl
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--email', default=None)
parser.add_argument('--password', default=None)
parser.add_argument('--receiver', default=None)

args = parser.parse_args()

port = 465
password = args.password
sender_email = args.email
receiver_email = args.receiver

match_bank = [b'dsa', b'gmk', b'sa', b'oem', b'xsa', b'cherry Profile', b'caps', b'cap', b'keycap', b'keycaps', b'key cap', b'key caps', b'tai hao', b'laser', b'keysets', b'base']
request_in = feedparser.parse('http://www.reddit.com/r/mechmarket/new/.rss')
req_list = []
for curr_req in request_in.entries:
    string_comp = curr_req.title.encode('utf-8').lower()
    for i in match_bank:
            if i in string_comp.split(b' '):
                try:
                    if string_comp.split(b' ').index(b'[w]') > string_comp.split(b' ').index(i):
                        req_list.append(curr_req)
                        break
                except:
                        continue
            else: continue

messageblock = ""
for x in req_list:
    messageblock += x.title
    messageblock += "\n"
    messageblock += x.author_detail.name
    messageblock += "\n"
    messageblock += x.link
    messageblock += "\n"
    messageblock += "\n"

message = """\
Subject: /r/mechmarket: Recent Keycaps


"""

message += "{}\n".format(messageblock)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
