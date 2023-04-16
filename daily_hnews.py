import csv
import subprocess, os, platform
import requests
from bs4 import BeautifulSoup

import smtplib  # protocol
from email.message import EmailMessage
from string import Template
from pathlib import Path

YOUR_EMAIL_TO_SEND_FROM = ''
YOUR_APP_PASSWORD_GMAIL = ''
EMAIL_TO_RECEIVE = ''


response = requests.get('https://news.ycombinator.com')
response2 = requests.get('https://news.ycombinator.com?p=2')
soup = BeautifulSoup(response.text, 'html.parser')
soup2 = BeautifulSoup(response2.text, 'html.parser')

links = soup.select('.titleline > a')
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline > a')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2


def sort_stories_by_votes(hmlist):
    return sorted(hmlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []

    with open('index.html', 'r+') as fp:
        fp.truncate()
        fp.write('''
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <div class="alignment" align="center" style="line-height:10px"><img class="big" src="https://www.tagesspiegel.de/images/spongebob/alternates/BASE_16_9_W1400/spongebob.jpeg" style="display: block; height: auto; border: 0; width: 900px; max-width: 50%;" width="1500"></div>
    <h2>Good morning $name!</h2>
    <p>Keep up with the good mood by checking out the top HackerNews ratings!</p>
    <br>
''')
        for idx, item in enumerate(links):
            title = links[idx].getText()
            href = links[idx].get('href', None)
            vote = subtext[idx].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
                if points > 200:
                    row = {'title': title, 'link': href, 'votes': points}
                    hn.append(row)
        fp.write('''
    <p>Have a great day!</p>)
</body>
</html>
''')
    fp.close()
    return sort_stories_by_votes(hn)


all_news = create_custom_hn(mega_links, mega_subtext)

with open('today_news.txt', 'r+') as fp:
    fp.truncate()
    for i in all_news:
        fp.write(str(i)+'\n')
fp.close()


with open('index.html', 'r+') as fp:
    fp.truncate()
    fp.write('''<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <div class="alignment" align="center" style="line-height:10px"><img class="big" src="https://www.tagesspiegel.de/images/spongebob/alternates/BASE_16_9_W1400/spongebob.jpeg" style="display: block; height: auto; border: 0; width: 900px; max-width: 50%;" width="1500"></div>
    <h2>Good morning $name!</h2>
    <p>Keep up with the good mood by checking out the top HackerNews listings!</p>
    <br>
''')
    with open('today_news.txt', 'r') as fr:
        reader = csv.reader(fr)
        for row in reader:
            # print(row)
            for i in row:
                x = str(i.replace('''{\'title\': ''', '').replace('\'', '').replace(' link: ', '').replace(' votes: ', 'Votes: ').replace('}', '').replace('$', 'Dollar'))
                fp.write('    <p>'+str(x)+'</p>'+'\n')
            # print('')
            fp.write('    <br>'+'\n')
    fr.close()
    fp.write('''
    <p>Have a great day!</p>)
</body>
</html>
''')
fp.close()


def send_mail():
    email_list = [EMAIL_TO_RECEIVE]

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()  # connect securely to the server
        smtp.login(YOUR_EMAIL_TO_SEND_FROM, YOUR_APP_PASSWORD_GMAIL)

        for mail in email_list:
            html = Template(Path('index.html').read_text())
            email = EmailMessage()
            email['from'] = 'kit4py'
            email['to'] = mail
            email['subject'] = 'Hacker News!'

            email.set_content(html.substitute({'name': 'User273'}), 'html')
            print(f'sent to: {mail}')

            smtp.send_message(email)
        print('=== completed! ===')


def open_txt():
    filepath = 'today_news.txt'
    if platform.system() == 'Darwin':  # macOS
        os.system('clear')
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))


if __name__ == '__main__':
    os.system('clear')
    print('''
   __ ___  _____                     
  / // / |/ / _ \___ ___________ ____
 / _  /    / ___/ _ `/ __(_-/ -_/ __/
/_//_/_/|_/_/   \_,_/_/ /___\__/_/   
                                         
''')
    task = int(input('''
[1] send results to email
[2] show results in txt
Enter number: '''))

    if task == 1:
        send_mail()
    elif task == 2:
        open_txt()
    else:
        print('wrong number')
