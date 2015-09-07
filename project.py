import requests
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import urllib
import pdb

def getSnowballEffect():
	winningdiff_early 
	winningdiff_mid													  
	losingdiff_early 
	losingdiff_mid 
	
	avgGood = 0
	avgBad = 0
	
	for index in range (0,len(winningdiff_early)):
		newNumA = winningdiff_early[index]
		newNumB = winningdiff_mid[index]
		if newNumA > 0 :
			if newNumA < newNumB:
				if newNumA/newNumB > 0.5:
					avgGood += newNumB - newNumA
				else : 
					avgGood += newNumA
			else :	
				toAdd = newNumA-newNumB
				if toAdd <= newNumA:
					avgGood -= toAdd
				else:
					avgGood -= newNumA
		else:
			newNumA = -newNumA			
			newNumB = -newNumB
			if newNumA < newNumB:
				if newNumA/newNumB > 0.5:
					avgGood += newNumB - newNumA
				else : 
					avgGood += newNumA
			else :	
				toAdd = newNumA-newNumB
				if toAdd <= newNumA:
					avgGood -= toAdd
				else:
					avgGood -= newNumA
	
	for index in range (0,len(losingdiff_early)):
		newNumA = losingdiff_early[index]
		newNumB = losingdiff_mid[index]
		if newNumA > 0 :
			if newNumA < newNumB:
				if newNumA/newNumB > 0.5:
					avgBad += newNumB - newNumA
				else : 
					avgBad += newNumA
			else :	
				toAdd = newNumA-newNumB
				if toAdd <= newNumA:
					avgBad -= toAdd
				else:
					avgBad -= newNumA
		else:
			newNumA = -newNumA			
			newNumB = -newNumB
			if newNumA < newNumB:
				if newNumA/newNumB > 0.5:
					avgBad += newNumB - newNumA
				else : 
					avgBad += newNumA
			else :	
				toAdd = newNumA-newNumB
				if toAdd <= newNumA:
					avgBad -= toAdd
				else:
					avgBad -= newNumA
	if avgGood != 0:
		avgGood = avgGood/len(winningdiff_early)
	if avgBad != 0:	
		avgBad = avgBad/len(losingdiff_early)
	thislist = [avgGood,avgBad]
	return thislist

def getSummonerId():
	summoner_initial = raw_input('Enter summoner name lowercase and without spaces : ')
	summoner = urllib.quote(summoner_initial)
	summoner_url = url + 'v1.4/summoner/by-name/' + summoner

	response1 = requests.get(summoner_url + '?' + key)
	results = response1.json()
	summoner_id = results[summoner]['id']

	print summoner_id
	time.sleep(1)
	return summoner_id


def getMatchList():
	games = raw_input("Please enter sample size : ")
	que_type = '?rankedQueues=RANKED_SOLO_5x5&'
	indices = 'beginIndex=0&endIndex=' + str(games)+'&'
	response2 = requests.get(url+'v2.2/matchlist/by-summoner/' + str(summoner_id) +que_type + indices +key)
	while response2.status_code != 200:
		print response2.status_code
		time.sleep(60)
		response2 = requests.get(url+'v2.2/matchlist/by-summoner/' + str(summoner_id) +que_type + indices +key)
	print response2.status_code
	matchcontainer = response2.json()
	role = raw_input("Please type in JUNGLE, MID, TOP, or BOTTOM in that same format : ")
	for match in matchcontainer['matches']:
		if match['lane'] == role:
			match_ids.append(match['matchId'])
	for number in match_ids:
		print number
	print str(len(match_ids)) + " Games as a " + role
	return role

def getXpDiff():
	clearList()
	requestType = 'v2.2/match/'
	printnumber = 0
	for matchnumber in match_ids:
		response3 = requests.get(url+requestType+str(matchnumber)+'?includeTimeline=true&'+key)
		time.sleep(1)
		while response3.status_code != 200:
			print response3.status_code
			if response3.status_code == 429:
				time.sleep(20)
			else:
				break
			response3 = requests.get(url+requestType+str(matchnumber)+'?includeTimeline=true&'+key)
		matchinfo = response3.json()
		print printnumber
		printnumber += 1
		for indiv_stats in matchinfo['participants']:
			if indiv_stats['timeline']['lane'] == role:
				if 'xpDiffPerMinDeltas' in indiv_stats['timeline']:
					if 'tenToTwenty'  not in indiv_stats['timeline']['xpDiffPerMinDeltas']:
						break
				else: 
					break
				if indiv_stats['stats']['winner'] :
					winningdiff_early.append(indiv_stats['timeline']['xpDiffPerMinDeltas']['zeroToTen'])
					winningdiff_mid.append(indiv_stats['timeline']['xpDiffPerMinDeltas']['tenToTwenty'])
					
					break
				else :
					losingdiff_early.append(indiv_stats['timeline']['xpDiffPerMinDeltas']['zeroToTen'])
					losingdiff_mid.append(indiv_stats['timeline']['xpDiffPerMinDeltas']['tenToTwenty'])
					
					break
				

def clearList():
	del winningdiff_early[:]
	del winningdiff_mid[:]
	del losingdiff_early[:]
	del losingdiff_mid[:]
	
def plotStuff(list1,list2,lista,listb):
	
	length1 = []
	length2 = []
	for i in range (len(list1)):
		length1.append(i)
	for i in range (len(lista)):
		length2.append(i)
	plt.figure(1)
	plt.subplot(211)
	plt.plot(length1,list1,'ro',label = '0-10 Mins')
	plt.plot(length1,list2,'bo',label = '10-20 Mins')
	plt.plot((0,len(list1)),(avg(list1),avg(list1)), 'r-', 
			 (0,len(list1)),(avg(list2),avg(list2)),'b-',
			 (0, len(list1)), (0,0),'g-')
	plt.title ('Winning xp differences 0-10,10-20 for player : ' + str(summoner_id))
	plt.axis([0,len(list1),-350,350])
	plt.ylabel('XP Difference/Minute')
	plt.legend()
	plt.text(0.1,280, ('Snowball effect: ' + str(int(snowball[0])) + ' , ' + 
					   str(int(snowball[1]))) , fontsize = 13)
	plt.subplot(212)
	plt.plot(length2,lista,'ro',length2,listb,'bo',(0,len(lista)),(avg(lista),avg(lista)), 'r-', 
			(0,len(lista)),(avg(listb),avg(listb)),'b-',
			(0, len(lista)), (0,0),'g-')
	plt.title('Losing xp differences 0-10,10-20')
	plt.axis([0,len(lista),-350,350])
	plt.ylabel('XP Difference/Minute')
	plt.legend()
	plt.show()
	print 'Average xpDiff 0-10 for wins : ',
	print avg(list1)
	print 'Average xpDiff 10-20 for wins : ',
	print avg(list2)
	print 'Average xpDiff 0-10 for losses : ',
	print avg(lista)
	print 'Average xpDiff 10-20 for losses : ',
	print avg(listb)
	print 'Average snowball effect for good starts : ' + str(snowball[0])
	print 'Average snowball effect for bad starts : ' + str(snowball[1])

def avg(list):
	average = 0
	for number in list:
		average += number
	if len(list) != 0:	
		return average / len(list)	
				
key = 'api_key=b77f2e1b-ef99-4b51-a40f-7eae9d4fb72b'
url = 'https://na.api.pvp.net/api/lol/na/'
winningdiff_early = []
winningdiff_mid =[]														  
losingdiff_early = []
losingdiff_mid = []
match_ids = []
snowball = []

summoner_id = getSummonerId()
role = getMatchList()
if role == 'MID':
	role = 'MIDDLE'
getXpDiff()
snowball = getSnowballEffect()

plotStuff(winningdiff_early,winningdiff_mid,losingdiff_early,losingdiff_mid)



#print matchcontainer['matches'][0]['participants']


	


