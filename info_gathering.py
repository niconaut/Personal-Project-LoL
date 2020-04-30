import custom_functions as riot
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import time
from itertools import chain
import psycopg2
from sqlalchemy import create_engine

# BASIC INFORMATION
accountId = 'NP5LxDYBJF3W5Otjc7RRkT-gpy8DQB6dYoMjmMeXjqGjcQ'
beginTime = str(int(datetime.timestamp(datetime(2020, 1, 15)))) # opening date of fun mode
region = 'na1'
API_KEY = 'RGAPI-e95b222b-6155-40ef-adfa-b806b86f38c0' # expires daily so no worries

# summoner names
summoner_names = ['Blu','Zubits','CptFuzz','Dejoing','SaltineIV']


# SUMMONER INFORMATION
summoner_list = []
for name in summoner_names:
    summoner_list.append(riot.summoner_data_name(summoner_name=name,API_KEY=API_KEY,region='na1'))
summoner_df = pd.DataFrame(summoner_list)

# saving the dataframe into PostgreSQL
engine = create_engine('postgresql://username:password@localhost/riot_api')
summoner_df.to_sql(name='summonerInformation',con=engine,if_exists='replace',index=False)


# GETTING URF MATCHES
URF = riot.get_URF(accountId=accountId,beginTime=beginTime,API_KEY=API_KEY)
dfURF = pd.DataFrame(URF['matches'])
dfURF.insert(2,'accountId',accountId)

# URF match list
URFmatches = [str(x) for x in list(dfURF['gameId'])]


# GENERAL MATCH INFORMATION
a = []
for match in URFmatches:
    a.append(riot.match_information(match,API_KEY))
    time.sleep(1.5)
matchInformation = pd.DataFrame(a)

# saving the dataframe into PostgreSQL
engine = create_engine('postgresql://username:password@localhost/riot_api')
matchInformation.to_sql(name='matchInformation',con=engine,if_exists='replace',index=False) # if_exists=append


# TEAM INFORMATION
a = []
for match in URFmatches:
    a.append(riot.team_information(match,API_KEY))
    time.sleep(1.5)
teamInformation = pd.DataFrame(list(chain.from_iterable(a)))

# saving the dataframe into PostgreSQL
engine = create_engine('postgresql://username:password@localhost/riot_api')
teamInformation.to_sql(name='teamInformation',con=engine,if_exists='replace',index=False) # if_exists=append


# SUMMONERS INFORMATION
a = []
for match in URFmatches:
    a.append(riot.summoner_information(match,API_KEY))
    time.sleep(1.5)
summonerMatchInformation = pd.DataFrame(list(chain.from_iterable(a)))

# saving the dataframe into PostgreSQL
engine = create_engine('postgresql://username:password@localhost/riot_api')
summonerMatchInformation.to_sql(name='summonerMatchInformation',con=engine,if_exists='replace',index=False)


# POST PARTICIPANTS INFORMATION
a = []
for match in URFmatches:
    a.append(riot.post_participants_information(match,API_KEY))
    time.sleep(1.5)
postParticipantInfo = pd.DataFrame(list(chain.from_iterable(a)))
PPI_df = postParticipantInfo

dict_cols = ['creepsPerMinDeltas','xpPerMinDeltas','goldPerMinDeltas','csDiffPerMinDeltas','xpDiffPerMinDeltas','damageTakenPerMinDeltas','damageTakenDiffPerMinDeltas']
time_deltas = ['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100','100-110','110-120']

for column in dict_cols:
    PPI_df = pd.concat([PPI_df.drop([column], axis=1), PPI_df[column].apply(pd.Series)], axis=1)
    PPI_df.drop(0, 1, inplace = True)
    for time in time_deltas:
        PPI_df.rename(columns = {time:time + '_' + column}, inplace = True)

# saving the dataframe into PostgreSQL
engine = create_engine('postgresql://username:password@localhost/riot_api')
PPI_df.to_sql(name='postParticipantInfo',con=engine,if_exists='replace',index=False) # if_exists=append


# MATCH EVENTS
a = []
for match in URFmatches:
    a.append(riot.match_events(match,API_KEY))
    time.sleep(1.5)
matchEvents = pd.DataFrame(list(chain.from_iterable(a)))
ME_df = matchEvents

ME_df = pd.concat([ME_df.drop(['position'], axis=1), ME_df['position'].apply(pd.Series)], axis=1)
ME_df.drop(0,1,inplace = True)
ME_df.rename(columns = {'x':'x_position', 'y':'y_position'}, inplace = True)

ME_df = pd.concat([ME_df.drop(['assistingParticipantIds'], axis=1), ME_df['assistingParticipantIds'].apply(pd.Series)], axis=1)
ME_df.rename(columns = {0:'assistingParticipantId1',1:'assistingParticipantId2',2:'assistingParticipantId3',3:'assistingParticipantId4'}, inplace = True)

# saving the dataframe into PostgreSQL
engine = create_engine('postgresql://username:password@localhost/riot_api')
ME_df.to_sql(name='matchEvents',con=engine,if_exists='replace',index=False) # if_exists=append


# MATCH TIMELINE
a = []
for match in URFmatches:
    a.append(riot.match_timeline(match,API_KEY))
    time.sleep(1.5)
matchTimeline = pd.DataFrame(list(chain.from_iterable(a)))
MT_df = matchTimeline

MT_df = pd.concat([matchTimeline.drop(['position'],axis=1),matchTimeline['position'].apply(pd.Series)],axis=1)
MT_df.drop(0,1,inplace = True)
MT_df.rename(columns = {'x':'x_position', 'y':'y_position'}, inplace = True)

# saving the dataframe into PostgreSQL
engine = create_engine('postgresql://username:password@localhost/riot_api')
MT_df.to_sql(name='matchTimeline',con=engine,if_exists='replace',index=False) # if_exists=append