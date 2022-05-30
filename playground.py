import os
import pandas as pd
import json
import requests
from datetime import datetime

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
leagueId = '1040456'

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
                'transers_in','transfer_out','captain','vice_captain','multiplier','team_name','total_gameweek_points','rank','manager','squad_id','gameweek'])

    rowCounter = 0
    for row in df.total_points:
        x = df.iloc[rowCounter]['multiplier']
        newPoints = row * x
        df.loc[rowCounter,['total_points']] = newPoints

        rowCounter += 1

    df.to_excel(f'twenty ten results gameweek {current_gw}.xlsx')






if __name__ == '__main__':
    leagueDataYN = input('get league data? (Y/N): ')
    if leagueDataYN == 'Y':
        leagueResponse = leagueData(leagueId)

    topLevelDataYN = input('get top level data? (Y/N): ')
    if topLevelDataYN == 'Y':
        topLevelResponse = topLevelData(url)

    squadDataYN = input('get squad level data? (Y/N): ')
    if squadDataYN == 'Y':
        topLevelResponse = topLevelData(url)
        eventsDF = topLevelResponse[2]
        playersDF = topLevelResponse[0]
        leagueResponse = leagueData(leagueId)
        squadData(leagueResponse,eventsDF,playersDF)

