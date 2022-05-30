import pandas as pd
import json,requests,psycopg2,os,uuid
from datetime import datetime
from decouple import config

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
leagueId = config('LEAGUEID')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

""" SQUAD STATS SECTION """
nameSquadList = []
elementSquadList = []
totalPointsSquadList = []
minutesSquadList = []
goalsSquadList = []
assistsSquadList = []
cleanSheetsSquadList = []
goalsConcededSquadList = []
ownGoalsSquadList = []
penaltiesSavedSquadList = []
penaltiesMissedSquadList = []
yellowCardsSquadList = []
redCardsSquadList = []
savesSquadList = []
bonusSquadList = []
bpsSquadList = []
influenceSquadList = []
creativitySquadList = []
threatSquadList = []
ict_indexSquadList = []
valuesSquadList = []
selectedSquadList = []
transfersInSquadList = []
transfersOutSquadList = []
captainSquadList = []
viceCaptainSquadList = []
multiplierSquadList = []
entryNameSquadList = []
eventTotalSquadList = []
rankSquadList = []
twentyTenNameSquadList = []
entrySquadList = []
gameweeklist = []


def topLevelData(url):
    response = requests.get(url)
    response = json.loads(response.content)

    players = response['elements']
    teams = response['teams']
    events = response['events']
    players_df = pd.DataFrame(players)
    teams_df = pd.DataFrame(teams)
    events_df = pd.DataFrame(events)

    events_df['deadline_time'] = pd.to_datetime(events_df['deadline_time'])
    events_df['deadline_time'] = events_df['deadline_time'].dt.tz_localize(None)
    return players_df,teams_df,events_df

def leagueData(leagueid):
    r = requests.get(f'https://fantasy.premierleague.com/api/leagues-classic/{leagueid}/standings')
    r = json.loads(r.content)
    teamData = r['standings']['results']

    df = pd.DataFrame()

    df['id'] = [team['id'] for team in teamData]
    df['event_total'] = [team['event_total'] for team in teamData]
    df['player_name'] = [team['player_name'] for team in teamData]
    df['rank'] = [team['rank'] for team in teamData]
    df['last_rank'] = [team['last_rank'] for team in teamData]
    df['rank_sort'] = [team['rank_sort'] for team in teamData]
    df['total'] = [team['total'] for team in teamData]
    df['entry'] = [team['entry'] for team in teamData]
    df['entry_name'] = [team['entry_name'] for team in teamData]
    return df

def squadData(leagueDf,events_df,players_df):
    squadIds = leagueDf['entry']
    now = datetime.now()
    current_gw = events_df[events_df['deadline_time'] < now]['id'].max()
    dfCounter = 0

    for id in squadIds:
        my_team_url = f'https://fantasy.premierleague.com/api/entry/{id}/event/{str(current_gw)}/picks/'
        response = requests.get(my_team_url)

        r = json.loads(response.content)
        picks = r['picks']
        for pick in picks:
            url = f"https://fantasy.premierleague.com/api/element-summary/{pick['element']}/"
            response = requests.get(url)
            response = json.loads(response.content)
            historyDict = response['history']

            Query = players_df.loc[players_df['id'] == pick['element']]


            is_captain = pick['is_captain']
            is_vice_captain = pick['is_vice_captain']
            multiplier = pick['multiplier']
            name = str(Query['first_name'].values[0] + ' ' + Query['second_name'].values[0])

            for i in historyDict:
                if i['round'] == current_gw:
                    gameweeklist.append(current_gw)
                    nameSquadList.append(name)
                    elementSquadList.append(i['element'])
                    totalPointsSquadList.append(i['total_points'])
                    minutesSquadList.append(i['minutes'])
                    goalsSquadList.append(i['goals_scored'])
                    assistsSquadList.append(i['assists'])
                    cleanSheetsSquadList.append(i['clean_sheets'])
                    goalsConcededSquadList.append(i['goals_conceded'])
                    ownGoalsSquadList.append(i['own_goals'])
                    penaltiesSavedSquadList.append(i['penalties_saved'])
                    penaltiesMissedSquadList.append(i['penalties_missed'])
                    yellowCardsSquadList.append(i['yellow_cards'])
                    redCardsSquadList.append(i['red_cards'])
                    savesSquadList.append(i['saves'])
                    bonusSquadList.append(i['bonus'])
                    bpsSquadList.append(i['bps'])
                    influenceSquadList.append(i['influence'])
                    creativitySquadList.append(i['creativity'])
                    threatSquadList.append(i['threat'])
                    ict_indexSquadList.append(i['ict_index'])
                    valuesSquadList.append(i['value'])
                    selectedSquadList.append(i['selected'])
                    transfersInSquadList.append(i['transfers_in'])
                    transfersOutSquadList.append(i['transfers_out'])
                    captainSquadList.append(is_captain)
                    viceCaptainSquadList.append(is_vice_captain)
                    multiplierSquadList.append(multiplier)
                    entryNameSquadList.append(leagueDf['entry_name'][dfCounter])
                    eventTotalSquadList.append(leagueDf['event_total'][dfCounter])
                    rankSquadList.append(leagueDf['rank'][dfCounter])
                    twentyTenNameSquadList.append(leagueDf['player_name'][dfCounter])
                    entrySquadList.append(leagueDf['entry'][dfCounter])

        dfCounter += 1

    df = pd.DataFrame(list(zip(nameSquadList,elementSquadList,totalPointsSquadList,minutesSquadList,goalsSquadList,
                               assistsSquadList,cleanSheetsSquadList,goalsConcededSquadList,ownGoalsSquadList,penaltiesSavedSquadList,
                               penaltiesMissedSquadList,yellowCardsSquadList,redCardsSquadList,savesSquadList,
                               bonusSquadList,bpsSquadList,influenceSquadList,creativitySquadList,threatSquadList,ict_indexSquadList,
                               valuesSquadList,selectedSquadList,transfersInSquadList,transfersOutSquadList,captainSquadList,
                               viceCaptainSquadList,multiplierSquadList,entryNameSquadList,eventTotalSquadList,rankSquadList,twentyTenNameSquadList
                               ,entrySquadList,gameweeklist
    )),columns=['name','element','total_points','minutes','goals','assists','clean_sheets','goals_conceded','own_goals','penalties_saved'
                ,'penalties_missed','yellow_cards','red_cards','saves','bonus','bps','influence','creativity','threat','ict','values','selected',
                'transfers_in','transfer_out','captain','vice_captain','multiplier','team_name','total_gameweek_points','rank','manager','squad_id','gameweek'])

    rowCounter = 0
    for row in df.total_points:
        x = df.iloc[rowCounter]['multiplier']
        newPoints = row * x
        df.loc[rowCounter,['total_points']] = newPoints
        rowCounter += 1

    dfCounterTwo = 0
    for i in df['name']:
        conn = psycopg2.connect(database=config('DB_NAME'), user=config('DB_USER'),password=config('DB_PASSWORD'), host=config('DB_HOST'))

        sqlSelect = f'SELECT * FROM public."datacollection_squadsdatamodel" WHERE "entryName" ='
        sqlSelectpt2 = f"'{str(df['team_name'].iloc[dfCounterTwo])}'"
        sqlSelector3 = f'AND "gameweek" = '
        sqlSelector4 = f" '{str(df['gameweek'].iloc[dfCounterTwo])}'"
        sqlSelector5 = f'AND "nameSquad" ='
        sqlSelector6 = f" '{str(df['name'].iloc[dfCounterTwo])}';"
        sqlCommandSelect = str(sqlSelect + sqlSelectpt2 + sqlSelector3 + sqlSelector4 + sqlSelector5 + sqlSelector6)

        cursor = conn.cursor()
        cursor.execute(sqlCommandSelect)
        response = cursor.fetchall()

        if response == []:
            uuidVar = uuid.uuid4()
            sqlInsert = 'INSERT INTO public."datacollection_squadsdatamodel"("UUID","gameweek","nameSquad","element","totalPoints","minutes","goals","assists","cleanSheets","goalsConceded","ownGoals","penaltiesSaved","penaltiesMissed","yellowCards","redCards","saves","bonus","bps","influence","creativity","threat","ict_index","values","selected","transfersIn","transfersOut","captain","viceCaptain","multiplier","entryName","eventTotal","rank","twentyTenName","entry")'

            sqlValues = f"VALUES('{uuidVar}','{df['gameweek'].iloc[dfCounterTwo]}','{df['name'].iloc[dfCounterTwo]}','{df['element'].iloc[dfCounterTwo]}','{df['total_points'].iloc[dfCounterTwo]}','{df['minutes'].iloc[dfCounterTwo]}','{df['goals'].iloc[dfCounterTwo]}','{df['assists'].iloc[dfCounterTwo]}','{df['clean_sheets'].iloc[dfCounterTwo]}','{df['goals_conceded'].iloc[dfCounterTwo]}','{df['own_goals'].iloc[dfCounterTwo]}','{df['penalties_saved'].iloc[dfCounterTwo]}','{df['penalties_missed'].iloc[dfCounterTwo]}','{df['yellow_cards'].iloc[dfCounterTwo]}','{df['red_cards'].iloc[dfCounterTwo]}','{df['saves'].iloc[dfCounterTwo]}','{df['bonus'].iloc[dfCounterTwo]}','{df['bps'].iloc[dfCounterTwo]}','{df['influence'].iloc[dfCounterTwo]}','{df['creativity'].iloc[dfCounterTwo]}','{df['threat'].iloc[dfCounterTwo]}','{df['ict'].iloc[dfCounterTwo]}','{df['values'].iloc[dfCounterTwo]}','{df['selected'].iloc[dfCounterTwo]}','{df['transfers_in'].iloc[dfCounterTwo]}','{df['transfer_out'].iloc[dfCounterTwo]}','{df['captain'].iloc[dfCounterTwo]}','{df['vice_captain'].iloc[dfCounterTwo]}','{df['multiplier'].iloc[dfCounterTwo]}','{df['team_name'].iloc[dfCounterTwo]}','{df['total_gameweek_points'].iloc[dfCounterTwo]}','{df['rank'].iloc[dfCounterTwo]}','{df['manager'].iloc[dfCounterTwo]}','{df['squad_id'].iloc[dfCounterTwo]}');"
            sqlCommand = str(sqlInsert + sqlValues)

            with conn:
                cur = conn.cursor()
                cur.execute(sqlCommand)

        else:
            sqlUpdate = 'UPDATE public."datacollection_squadsdatamodel" SET "totalPoints"'
            sqlUpdate2 = f"= '{df['total_points'].iloc[dfCounterTwo]}', "
            sqlUpdate3 = '"minutes" ='
            sqlUpdate4 = f" '{df['minutes'].iloc[dfCounterTwo]}', "
            sqlUpdate5 = '"goals" ='
            sqlUpdate6 = f" '{df['goals'].iloc[dfCounterTwo]}', "
            sqlUpdate7 = '"assists" ='
            sqlUpdate8 = f" '{df['assists'].iloc[dfCounterTwo]}', "
            sqlUpdate9 = '"cleanSheets" ='
            sqlUpdate10 = f" '{df['clean_sheets'].iloc[dfCounterTwo]}', "
            sqlUpdate11 = '"goalsConceded" ='
            sqlUpdate12 = f" '{df['goals_conceded'].iloc[dfCounterTwo]}', "
            sqlUpdate13 = '"ownGoals" ='
            sqlUpdate14 = f" '{df['own_goals'].iloc[dfCounterTwo]}', "
            sqlUpdate15 = '"penaltiesSaved" ='
            sqlUpdate16 = f" '{df['penalties_saved'].iloc[dfCounterTwo]}', "
            sqlUpdate17 = '"penaltiesMissed" ='
            sqlUpdate18 = f" '{df['penalties_missed'].iloc[dfCounterTwo]}', "
            sqlUpdate19 = '"yellowCards" ='
            sqlUpdate20 = f" '{df['yellow_cards'].iloc[dfCounterTwo]}', "
            sqlUpdate21 = '"redCards" ='
            sqlUpdate22 = f" '{df['red_cards'].iloc[dfCounterTwo]}', "
            sqlUpdate23 = '"saves" ='
            sqlUpdate24 = f" '{df['saves'].iloc[dfCounterTwo]}', "
            sqlUpdate25 = '"bonus" ='
            sqlUpdate26 = f" '{df['bonus'].iloc[dfCounterTwo]}', "
            sqlUpdate27 = '"bps" ='
            sqlUpdate28 = f" '{df['bps'].iloc[dfCounterTwo]}', "
            sqlUpdate29 = '"influence" ='
            sqlUpdate30 = f" '{df['influence'].iloc[dfCounterTwo]}', "
            sqlUpdate31 = '"creativity" ='
            sqlUpdate32 = f" '{df['creativity'].iloc[dfCounterTwo]}', "
            sqlUpdate33 = '"threat" ='
            sqlUpdate34 = f" '{df['threat'].iloc[dfCounterTwo]}', "
            sqlUpdate35 = '"ict_index" ='
            sqlUpdate36 = f" '{df['ict'].iloc[dfCounterTwo]}', "
            sqlUpdate37 = '"values" ='
            sqlUpdate38 = f" '{df['values'].iloc[dfCounterTwo]}', "
            sqlUpdate39 = '"selected" ='
            sqlUpdate40 = f" '{df['selected'].iloc[dfCounterTwo]}', "
            sqlUpdate41 = '"transfersIn" ='
            sqlUpdate42 = f" '{df['transfers_in'].iloc[dfCounterTwo]}', "
            sqlUpdate43 = '"transfersOut" ='
            sqlUpdate44 = f" '{df['transfer_out'].iloc[dfCounterTwo]}', "
            sqlUpdate45 = '"multiplier" ='
            sqlUpdate46 = f" '{df['multiplier'].iloc[dfCounterTwo]}', "
            sqlUpdate47 = '"eventTotal" ='
            sqlUpdate48 = f" '{df['total_gameweek_points'].iloc[dfCounterTwo]}', "
            sqlUpdate49 = '"rank" ='
            sqlUpdate50 = f" '{df['rank'].iloc[dfCounterTwo]}',"
            sqlUpdate51 =  '"captain" ='
            sqlUpdate52 = f" '{df['captain'].iloc[dfCounterTwo]}',"
            sqlUpdate53 = '"viceCaptain" ='
            sqlUpdate54 = f" '{df['vice_captain'].iloc[dfCounterTwo]}'"
            sqlUpdate55 = f'WHERE "entryName" ='
            sqlUpdate56 = f"'{str(df['team_name'].iloc[dfCounterTwo])}'"
            sqlUpdate57 = f'AND "gameweek" = '
            sqlUpdate58 = f" '{str(df['gameweek'].iloc[dfCounterTwo])}'"
            sqlUpdate59 = f' AND "nameSquad" = '
            sqlUpdate60 = f" '{str(df['name'].iloc[dfCounterTwo])}';"

            sqlCommandUpdate = str(sqlUpdate + sqlUpdate2 + sqlUpdate3 + sqlUpdate4 + sqlUpdate5 + sqlUpdate6 + sqlUpdate7 + sqlUpdate8 + sqlUpdate9 + sqlUpdate10
                                + sqlUpdate11 + sqlUpdate12 + sqlUpdate13 + sqlUpdate14 + sqlUpdate15 + sqlUpdate16 + sqlUpdate17 + sqlUpdate18 + sqlUpdate19 + sqlUpdate20
                                + sqlUpdate21 + sqlUpdate22 + sqlUpdate23 + sqlUpdate24 + sqlUpdate25 + sqlUpdate26 + sqlUpdate27 + sqlUpdate28 + sqlUpdate29 + sqlUpdate30
                                + sqlUpdate31 + sqlUpdate32 + sqlUpdate33 + sqlUpdate34 + sqlUpdate35 + sqlUpdate36 + sqlUpdate37 + sqlUpdate38 + sqlUpdate39 + sqlUpdate40
                                + sqlUpdate41 + sqlUpdate42 + sqlUpdate43 + sqlUpdate44 + sqlUpdate45 + sqlUpdate46 + sqlUpdate47 + sqlUpdate48 + sqlUpdate49 + sqlUpdate50
                                + sqlUpdate51 + sqlUpdate52 + sqlUpdate53 + sqlUpdate54 + sqlUpdate55 + sqlUpdate56 + sqlUpdate57 + sqlUpdate58 + sqlUpdate59 + sqlUpdate60)

            with conn:
                cur = conn.cursor()
                cur.execute(sqlCommandUpdate)

        dfCounterTwo += 1
        conn.close()

    for i in df['manager'].unique():
        conn = psycopg2.connect(database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'),host=config('DB_HOST'))

        sqlSelectCheckup = f'SELECT "nameSquad" FROM public."datacollection_squadsdatamodel" WHERE "twentyTenName" ='
        sqlSelectpt2Checkup = f"'{str(i)}'"
        sqlSelector3Checkup = f'AND "gameweek" = '
        sqlSelector4Checkup = f" '{str(current_gw)}';"
        sqlCommandSelectCheckup = str(sqlSelectCheckup + sqlSelectpt2Checkup + sqlSelector3Checkup + sqlSelector4Checkup)

        cursor = conn.cursor()
        cursor.execute(sqlCommandSelectCheckup)
        response = cursor.fetchall()

        if len(response) == 15:
            pass
        else:
            dfSquadChange = df[df['manager'] == i]
            squadListSQLResponse = str(response).replace('(','').replace(",)",'').replace('[','').replace("'",'').replace(']',"").split(",")
            squadListAPIResponse = [i for i in dfSquadChange['name']]

            for sqlPlayer in squadListSQLResponse:
                firstChar = sqlPlayer[0]
                if firstChar == ' ':
                    sqlPlayer = sqlPlayer[1:]

                if sqlPlayer not in squadListAPIResponse:
                    conn = psycopg2.connect(database=config('DB_NAME'), user=config('DB_USER'),password=config('DB_PASSWORD'),host=config('DB_HOST'))

                    sqlDelete = f'DELETE FROM public."datacollection_squadsdatamodel" WHERE "nameSquad" ='
                    sqlDelete1 = f"'{str(sqlPlayer)}'"
                    sqlDelete2 = 'AND "gameweek" = '
                    sqlDelete3 = f" '{str(current_gw)}'"
                    sqlDelete4 = 'AND "twentyTenName" = '
                    sqlDelete5 = f" '{str(i)}';"
                    sqlDeleteCommand = str(sqlDelete + sqlDelete1 + sqlDelete2 + sqlDelete3 + sqlDelete4 + sqlDelete5)

                    with conn:
                        cur = conn.cursor()
                        cur.execute(sqlDeleteCommand)
        conn.close()

if __name__ == '__main__':
    topLevelResponse = topLevelData(url)
    eventsDF = topLevelResponse[2]
    playersDF = topLevelResponse[0]
    leagueResponse = leagueData(leagueId)
    squadData(leagueResponse,eventsDF,playersDF)
