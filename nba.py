#! /usr/bin/env python3
import pickle
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
#File = open('nbadata.csv')
#Reader = csv.reader(File)
#Data = list(Reader)


class Game:
    def __init__ (self, year, month, day, away, home, startTime, url):
        self.year = year
        self.month = month
        self.day = day
        self.away = away
        self.home = home
        self.startTime = startTime
        self.url = url
        self.iden = iden

games = {}

with open ('nba.db', 'rb') as handle:
    games = pickle.load(handle)
    
'''num=0
for g in games:
    games[g].iden = num
    num+=1


fout = input('New file ready to be made. New database filename: ')

with open(fout, 'wb') as handle:
    pickle.dump(games, handle)'''






leftWidth = 55
rightWidth=7
while True:
    now = datetime.now()
    mo = now.month
    yr = now.year
    day = now.day
    i=''
    idenSubtract=0
    while True:
        foundOne = False
        if i!='A' and i!='B':
            print('TODAY\'S GAMES'.center(leftWidth + rightWidth, '-'))
        else:
            s = str(mo) + '-' + str(day) + ' GAMES'
            print(s.center(leftWidth + rightWidth, '-'))
        print('A... Load Another Date')
        if i!='B':
            print('B... Load Previous Day')

        for g in games:
            if int(games[g].month) == mo and int(games[g].day) == day:
                if not foundOne:
                    foundOne = True
                    idenSubtract = games[g].iden - 1
                print(str(games[g].iden - idenSubtract) + '... '+games[g].away + ' @ ' + games[g].home + ' - ' + games[g].startTime)
            elif foundOne:
                break
            
        i = input()
        if i=='a':
            i='A'
        if i=='b':
            i='B'
            
        if i=='A':
            mo = int(input('MM: '))
            day = int(input('DD: '))
        elif i=='B':
            yesterday = datetime.now() - timedelta(days=1)
            yr = yesterday.year
            mo = yesterday.month
            day = yesterday.day

        else:
            break

    selectedGame = int(i)+idenSubtract
    

    soup = BeautifulSoup((requests.get(games[selectedGame].url).text), "html.parser")

    spans = soup.find('span', {'class' : 'awayTeam-score'})
    aScore = spans.get_text()
    spans = soup.find('span', {'class' : 'homeTeam-score'})
    hScore = spans.get_text()
    tLine = ' ' + aScore + ' - ' + games[selectedGame].away + '   @   ' + games[selectedGame].home + ' - ' + hScore + ' '
    print(tLine.center(42,'='))
    

    # this is where we store the extracted data
    players = []

    # iterates through the table rows
    for row in soup.find_all('tr'):
        # this takes the text (which is seperated by \n in you case) 
        # and the "if data" is used to clean up empty entries
        player_data = [data for data in row.get_text().split("\n") if data]
        players.append(player_data)

    # we remove the first entry, as it's the table headers
    del players[0]
    i=0
    for player in players:
        if player[0] == 'Name':
            i=0
            print('\n')
        if player[1] == '0': #no minutes
            print (player[0].ljust(20) + 'DNP')
        else:
            if(i%2==0):
                charFiller = ' '
            else:
                charFiller = '-'
            print(player[0].ljust(20, charFiller) + player[1].ljust(6, charFiller) + player[2].ljust(6, charFiller) + player[3].ljust(6, charFiller) + player[4].rjust(3, charFiller))
        i+=1

    waiting = input('\nPress enter to continue')



#this function was used to match and assign a unique and proper url to every game in the database
'''
acronyms = ['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']
for i in range(1,1231):
    if i < 10:
        s = '000' + str(i)
    elif i<100:
        s = '00' + str(i)
    elif i<1000:
        s = '0' + str(i)
    else:
        s = str(i)
        
    url = 'http://mw.nba.com/feature/scores/boxscore/index.html?gameId=002160' + s + '&locale=en_US'
    res = requests.get(url)

    awayTeam=''
    homeTeam=''

    soup = bs4.BeautifulSoup(res.text)
    spans = soup.find_all('span', {'class' : 'awayTeam-code'})
    for team in acronyms:
        if team in str(spans):
            awayTeam = team
            print(awayTeam)


    spans = soup.find_all('span', {'class' : 'homeTeam-code'})
    for team in acronyms:
        if team in str(spans):
            homeTeam = team
            print(homeTeam)

    if homeTeam == '' or awayTeam == '':
        print('Team not found. Home: ' + homeTeam + ', Away: ' + awayTeam)
        wait = input()

    for g in games:
        if games[g].home == homeTeam and games[g].away == awayTeam and games[g].url == '':
            games[g].url = url
            print(games[g].url)
            break

fout = input('New file ready to be made. New database filename: ')

with open(fout, 'wb') as handle:
    pickle.dump(games, handle)'''












'''
#this function was to create a basic array of all games based on basketball-references posted full-season schedule

inti=0
for i in Data:

    
#parsing year
    date = Data[inti][0]
    if '2016' in date:
        year = '2016'
    elif '2017' in date:
        year = '2017'
    else:
        print('ERROR: COULD NOT FIND YEAR IN DATE. MAYBE WRONG INDEX')

    if 'Jan' in date:
        month = '01'
    elif 'Feb' in date:
        month = '02'
    elif 'Mar' in date:
        month = '03'
    elif 'Apr' in date:
        month = '04'
    elif 'Oct' in date:
        month = '10'
    elif 'Nov' in date:
        month = '11'
    elif 'Dec' in date:
        month = '12'


#day
    if date[9] != ' ':
        day = date[8] + date[9]
    else:
        day = '0' + date[8]

    acronyms = {
        'tlanta':'ATL',
        'oston':'BOS',
        'rooklyn':'BKN',
        'harlotte':'CHA',
        'hicago':'CHI',
        'leveland':'CLE',
        'allas':'DAL',
        'enver':'DEN',
        'etroit':'DET',
        'olden':'GSW',
        'ouston':'HOU',
        'ndiana':'IND',
        'lippers':'LAC',
        'akers':'LAL',
        'emphis':'MEM',
        'iami':'MIA',
        'ilwaukee':'MIL',
        'innesota':'MIN',
        'rleans':'NOP',
        'nicks':'NYK',
        'klahoma':'OKC',
        'rlando':'ORL',
        'hiladelphia':'PHI',
        'hoenix':'PHX',
        'ortland':'POR',
        'acramento':'SAC',
        'ntonio':'SAS',
        'oronto':'TOR',
        'Jazz':'UTA',
        'ashington':'WAS'}

    for key in acronyms:
        if key in Data[inti][4]:            
            home = acronyms[key]
            break

    for key in acronyms:
        if key in Data[inti][2]:            
            away = acronyms[key]
            break

    startTime = Data[inti][1]
    url = ''
    games[inti] = Game(year, month, day, away, home, startTime, url)
    inti+=1


fout = input('New file ready to be made. New database filename: ')

with open(fout, 'wb') as handle:
    pickle.dump(games, handle)


#0 date - tue oct 25 2016
#1 start time - 7:30 pm
#2 away team - New York Knicks
#3 away score - 88
#4 home team
#5 home score
#6 Box Score
#7 OT?
#8 Notes


    #pData format
    #0 year
    #1 month
    #2 day
    #3 away (formatted)
    #4 home (formatted)
    #5 start time
'''
