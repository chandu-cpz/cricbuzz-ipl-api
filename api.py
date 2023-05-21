import requests
from bs4 import BeautifulSoup
import datetime
import re
import streamlit as st
url = "https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/matches"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

match_results = []
match_links = ""
current_date = datetime.datetime.now().date()

#Try finding matches in the first class
for match in soup.find_all("div", {"class": "cb-col-100 cb-col cb-series-brdr cb-series-matches"}):
    match_date_elem = match.find("div", {"class": "cb-col-25 cb-col pad10 schedule-date"})
    if match_date_elem:
        timestam= match_date_elem.find("span")['ng-bind'].split("|")[0].strip()
        timestamp=int(timestam)
        match_date = datetime.datetime.fromtimestamp(timestamp/1000).date()
        if current_date == match_date:
            match_results.append(match)
            match_link_elem = match.find("a", {"class": "text-hvr-underline"})
            venue=match.find("div",{"class":""})
            match_link = "https://www.cricbuzz.com" + match_link_elem["href"]
            # check if match is in progress
            if match.find("a", {"class": "cb-text-inprogress"}):
                match_links=match_link
            #else:
                #match_links.append(match_link)

# If no matches were found in the first class, try the second class
for match in soup.find_all("div", {"class": "cb-col-100 cb-col cb-series-matches"}):
    match_date_elem = match.find("div", {"class": "cb-col-25 cb-col pad10"})
    if match_date_elem:
        timestam= match_date_elem.find("span")['ng-bind'].split("|")[0].strip()
        timestamp=int(timestam)
        match_date = datetime.datetime.fromtimestamp(timestamp/1000).date()
        if current_date == match_date:
            match_results.append(match)
            match_link_elem = match.find("a", {"class": "text-hvr-underline"})
            match_link = "https://www.cricbuzz.com" + match_link_elem["href"]
            # check if match is in progress
            if match.find("a", {"class": "cb-text-inprogress"}):
                match_links=match_link
            #else:
                #match_links.append(match_link)



if len(match_links)<=0:
    print("No matches are currently going on")
    st.header("No matches are currently going on comeback later")
else:
    url=match_links
    print("the url is: ")
    print(url)
    if(url==""):
        print("There is no matching ongoing")
        exit()
    else:
        response = requests.get(url)
        soup1 = BeautifulSoup(response.content, 'html.parser')
        teams=soup1.find("div",{"class":"cb-col cb-col-100 mrgn-btm-5"})
        teams_1=teams.find("a",{"class":"cb-mat-mnu-itm cb-ovr-flo"})
        all_teams=teams_1.text.strip()
        regex = r'([A-Z]{2,4})\s+vs\s+([A-Z]{2,3})'
        # find the matches using the regular expression
        match = re.search(regex,all_teams)
        if match:
            team1 = match.group(1)
            team2 = match.group(2)
            print(f'team1: {team1}, team2: {team2}')
        else:
            print('Unable to fetch team names')
        venue_div_div=soup1.find_all("div",{"class":"cb-nav-main cb-col-100 cb-col cb-bg-white"})
        for i in venue_div_div:
            venue_div=i.find("div",{"class":"cb-nav-subhdr cb-font-12"})
        venue_a = venue_div.find_all('a')[1]  # get the second <a> element within the div (after "Indian Premier League 2023")
        venue_text = venue_a.find('span', {'itemprop': 'name'}).text.strip()  # find the span element with itemprop='name' and extract its text
        print(venue_text)       
        scorecard = soup1.find('div', {'class': 'cb-col-scores'})
        score = scorecard.find('div', {'class': 'cb-min-bat-rw'}).text.strip()
        # create a multidimensional array to store player innings details
        player_innings = []

        rows_4=soup1.find_all('div',{'class':'cb-col cb-col-100 cb-min-itm-rw'})
        for row in rows_4:
            name = row.find('a',{'class':'cb-text-link'}).text.strip()
            runs_div = row.find_all("div")
            player_details = []
            for i in runs_div:
                player_details.append(i.text.strip())
            player_innings.append(player_details)

# print the player innings details from the array
        for player in player_innings:
            print(player[0])
            print("Runs: ", player[1])
            print("Balls: ", player[2])
            print("Fours: ", player[3])
            print("Sixes: ", player[4])
            print("Strike Rate: or Economy Rate ", player[5])

                
            
        print(score)
    

    scorex=score.split()


    batting_team, runs_and_wickets,overs,crr= scorex[0],scorex[1],scorex[2],scorex[4]
    try:
        req = scorex[6]
    except IndexError:
        req = 0
    runs,wickets=runs_and_wickets.split("/")

    print("Batting Team:", batting_team)
    if(batting_team==team1):
        bowling_team=team2
    else:
        bowling_team=team1
    print("Bowling Team:",bowling_team)
    print("Runs:", runs)
    print("Wickets:", wickets)

    match = re.search(r"\d+(\.\d+)?", overs)
    if match:
            float_val = float(match.group())
            print(float_val)
    overs=float_val

    print("Overs:", overs)
    print("Current Run Rate:", crr)
    if req:
        print("Required Run Rate:", req)
    else:
        print("Required Run Rate:",req)


    final_dict={}

    final_dict['url']=url
    final_dict['venue']=venue_text
    final_dict['batting_team']=batting_team
    final_dict['bowling_team']=bowling_team
    final_dict['runs']=int(runs)
    final_dict['wickets']=int(wickets)
    final_dict['overs']=overs
    final_dict['Current_RR']=crr
    final_dict['Required_RR']=req

    print(final_dict)
    st.write(final_dict)
    datetime.sleep(5)
    st.expirement_rerun()
