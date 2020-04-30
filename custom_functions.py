import requests
import numpy as np
# SUMMONER API CALLS

# SUMMONER DATA
def summoner_data_name(summoner_name,API_KEY,region='na1'):
    '''
    DOCSTRING: Gets summoner API data
    INPUT: region, summoner_name, API_KEY
    OUTPUT: dict with 7 key:values
    '''
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + API_KEY
    data = requests.get(URL)
    data = data.json()
    return data



# MATCHES API CALLS

# GET URF MATCHES
def get_URF(accountId,beginTime,API_KEY,region='na1'):
    '''
    DOCSTRING: Gets matches by accountId
    INPUT: accountId,beginTime,API_KEY,region
    OUTPUT: dict:list of matches,startIndex,endIndex,totalGames
    '''
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?api_key=' + API_KEY + '&queue=900' + '&beginTime=' + beginTime
    data = requests.get(URL)
    data = data.json()
    return data 

# GENERAL MATCH INFORMATION
def match_information(gameId,API_KEY,region='na1'):
    '''
    DOCSTRING: Gets general game information
    INPUT: region, gameId, API_KEY
    OUTPUT: dictionary of 10 key:values about one game
    '''
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + gameId + '?api_key=' + API_KEY 
    data = requests.get(URL)
    data = data.json()
    key_list = list(data.keys())[0:10]
    d = {}
    for key in key_list:
        d.update({key:data[key]})
    return d

# TEAM INFORMATION
def team_information(gameId,API_KEY,region='na1'):
    '''
    DOCSTRING: post game team information
    INPUT: region, gameId, API_KEY
    OUTPUT: list of dictionaries 17 key:values for each team per game
    '''
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + gameId + '?api_key=' + API_KEY 
    data = requests.get(URL)
    data = data.json()
    key_list = list(data['teams'][0].keys())
    l = []
    for i in np.arange(0,len(data['teams'])):
        d = {}
        d.update({'gameId':data['gameId']})
        for key in key_list:
            d.update({key:data['teams'][i][key]})
        l.append(d)
    return l

# SUMMONERS INFORMATION
def summoner_information(gameId,API_KEY,region='na1'):
    '''
    DOCSTRING: individual player information in the game
    INPUT: region, gameId, API_KEY
    OUTPUT: 10 key:values per player each game
    '''
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + gameId + '?api_key=' + API_KEY 
    data = requests.get(URL)
    data = data.json()
    player_list = list(data['participantIdentities'][0]['player'].keys())
    l = []
    for i in np.arange(0,len(data['participantIdentities'])):
        a = {}
        a.update({'gameId':data['gameId']})
        a.update({'participantId':data['participantIdentities'][i]['participantId']})
        for key in player_list:
            a.update({key:data['participantIdentities'][i]['player'][key]})
        l.append(a)
    return l

# POST MATCH INFORMATION/STATS
def post_participants_information(gameId,API_KEY,region="na1"):
    '''
    DOCSTRING: individual participant information in the game
    INPUT: region, gameId, API_KEY
    OUTPUT: 118 key:values for each player's post game information
    '''
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + gameId + '?api_key=' + API_KEY 
    data = requests.get(URL)
    data = data.json()
    participants_list = list(data['participants'][0].keys())[0:5]
    stats_list = list(data['participants'][0]['stats'].keys())
    deltas_list = list(data['participants'][0]['timeline'].keys())
    remove_list = list(set(participants_list) & set(stats_list))
    stats_list = [i for i in stats_list if i not in remove_list]
    deltas_list = [i for i in deltas_list if i not in remove_list]
    l = []
    for i in np.arange(0,len(data['participants'])):
        a = {}
        a.update({'gameId':data['gameId']})
        for key in participants_list:
            a.update({key:data['participants'][i][key]})
        for key in stats_list:
            a.update({key:data['participants'][i]['stats'][key]})
        for key in deltas_list:
            try:
                a.update({key:data['participants'][i]['timeline'][key]})
            except KeyError:
                continue
        l.append(a)
    return l

# MATCH EVENTS
def match_events(gameId,API_KEY,region='na1'):
    '''
    DOCSTRING: every event of each game
    INPUT: region, gameId, API_KEY
    OUTPUT: dict of each event in the game (one row, one event)
    '''
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/timelines/by-match/' + gameId + '?api_key=' + API_KEY
    data = requests.get(URL)
    data = data.json()
    event_list = []
    for i in np.arange(1,len(data['frames'])):
        for j in np.arange(0,len(data['frames'][i]['events'])):
            event_list += list(data['frames'][i]['events'][j].keys())
    event_list = set(event_list)
    l = []
    for i in np.arange(1,len(data['frames'])):
        for j in np.arange(0,len(data['frames'][i]['events'])):
            d = {}
            for key in event_list:
                try:
                    d.update({'gameId':gameId})
                    d.update({key:data['frames'][i]['events'][j][key]})
                except KeyError:
                    continue
            l.append(d)
    return l

# MATCH TIMELINE
def match_timeline(gameId,API_KEY,region='na1'):
    '''
    DOCSTRING: minute-by-minute summary of each player's information in game
    INPUT: region, gameId, API_KEY
    OUTPUT: minutes*10 outputs of 11 key:value pairs
    '''
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/timelines/by-match/' + gameId + '?api_key=' + API_KEY
    data = requests.get(URL)
    data = data.json()
    participant_nums = list(data['frames'][1]['participantFrames'].keys())
    p_frames_list = list(data['frames'][1]['participantFrames']['1'].keys())
    l = []
    for i in np.arange(0,len(data['frames'])):
        for num in participant_nums:
            d = {}
            d.update({'gameId':gameId})
            for key in p_frames_list:
                try:
                    d.update({key:data['frames'][i]['participantFrames'][num][key]})
                except KeyError:
                    continue
            l.append(d)
    return l