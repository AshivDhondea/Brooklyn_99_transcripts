# -*- coding: utf-8 -*-
"""
Created on Fri May  1 23:21:37 2020

Fetching transcripts for Brooklyn Nine Nine episodes
from brooklyn99.fandom.com

@author: Ashiv Hans Dhondea
"""

import requests
from bs4 import BeautifulSoup
import bleach
# --------------------------------------------------------------------------- #
# Set headers
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'})

def fnFetchSoup(episode_name):
    episode_url = "https://brooklyn99.fandom.com/wiki/"+episode_name+"/Transcript";
    req = requests.get(episode_url, headers);
    soup = BeautifulSoup(req.content, 'html.parser');
    return soup 

# --------------------------------------------------------------------------- #
episode_names = ["Boyle"+"'"+"s_Hunch",'Pilot','The_Slump','Halloween III','New_Captain','The_Oolong_Slayer','The_Tagger','The_Vulture']; 


for i_episode in range(0,len(episode_names)):
    soup = fnFetchSoup(episode_names[i_episode]);
    soup_list = (str(soup)).splitlines();
    
    raw_transcript = [];
    start_index = len(soup_list);
    
    for index in range(0,len(soup_list)):
        line = soup_list[index];
        
        # This indicates the start of the transcript
        if "mw-content-text" in line:
            start_index = index;
            
        if index > start_index:
            # Clean the lines in the html file
            line_bleached = bleach.clean(line, tags=[], attributes={}, styles=[], strip=True);
            line_bleached = line_bleached.strip();
            raw_transcript.append(line_bleached);
            
            # This is where the transcript ends. Delete irrelavant trailing lines
            if line_bleached == "NewPP limit report":
                del raw_transcript[-3:]
                break
             
    # --------------------------------------------------------------------------- #
    ## Write transcript to txt file.
    print('Writing to file: %s ' %episode_names[i_episode]);
    fname = episode_names[i_episode]+'_transcript.txt'
    with open(fname, mode='wt', encoding='utf-8') as myfile:
        for listitem in raw_transcript:
            myfile.write('%s\n' % listitem)
        
print('Cool Cool Cool')
