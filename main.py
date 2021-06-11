# messing with the youtube api

import requests

import re

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

KEY = os.environ.get("API_KEY")


def get_video(video_id, part=["snippet", "contentDetails", "statistics"]):
    part = "%2C".join(part)
    req = requests.get("https://youtube.googleapis.com/youtube/v3/videos?part=" + part + "&id=" + video_id + "&key=" + KEY)    

    if req.status_code == 200: # everything went as expected
        return req.json()["items"][0]
    else:
        print("Unexpected Status Code: " + req.status_code)
        return None

def get_comments(video_id):
    req = requests.get("https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId=" + video_id + "&key=" + KEY)

    if req.status_code == 200: # everything went as expected
        return req.json()["items"]
    else:
        print("Unexpected Status Code: " + req.status_code)
        return None

def get_search(keyword): # 
    req = requests.get("https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q=" + keyword + "&key=" + KEY)

    if req.status_code == 200: # everything went as expected
        return req.json()["items"]
    else:
        print("Unexpected Status Code: " + req.status_code)
        return None


def format_duration(dur):
    match = re.match("PT(?:(\d+)H)?(?:(\d+)M)?(\d+)S", dur)
    out = []    
    
    for group in match.groups():
        if group == None: continue
        elif len(group) < 2:
            out.append("0" + group)
        else:
            out.append(group)
    
    return ":".join(out)

def format_video_string(video):
    return "[ " + format_duration(video["contentDetails"]["duration"]) + " ] ( " + video["snippet"]["channelTitle"] + " ) \"" + video["snippet"]["title"] + "\""

def print_comments(com):
    for i in range(len(com)):
        msg_text = "\"" + com[i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"] + "\""
        msg_text = msg_text.replace("\n", " \\ ")

        print("[ " + com[i]["snippet"]["topLevelComment"]["snippet"]["publishedAt"] + " ] (" + com[i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"] + ") " + msg_text)

def print_search(search):
    for i in range(len(search)):
        print(str(i) + " : " + search[i]["id"]["videoId"] + " : " + format_video_string(get_video(search[i]["id"]["videoId"])))


while True:
    args = input("> ").split(" ")
    cmd = args.pop(0)
    
    if cmd == "get":
        subcmd = args.pop(0)
        if subcmd == "video":
            video = get_video(args[0])
            print(format_video_string(video))
        elif subcmd == "comments":
            comments = get_comments(args[0])
            print_comments(comments)
    elif cmd == "search":
        search = get_search(" ".join(args))
        print_search(search)
    elif cmd == "exit":
        break
    
    print("")

