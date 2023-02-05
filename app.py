from fastapi import FastAPI
import interface as elt
import json

app=FastAPI()
platforms={'amazon': elt.amazon, 'disney': elt.disney, 'hulu': elt.hulu, 'netflix': elt.netflix}

@app.get('/api/{platform}')
def findby_keyword(platform:str, keyword: str):
    return elt.findby_keyword(platforms[platform], keyword)

@app.get('/api/{platform}/')
def findby_score_per_year(platform:str, year:int, score:int):
    return elt.findby_score_per_year(platforms[platform], year, score)

@app.get('/api/maxscore2/{platform}')
def find_second_max_score(platform:str):
    return json.loads(elt.find_second_max_score(platforms[platform]))

@app.get('/api/maxduration/{platform}')
def findby_max_duration(platform:str, duration_type:str):
    return json.loads(elt.findby_max_duration(platforms[platform], duration_type))

@app.get('/api/qtybyrating/{platform}')
def qty_by_rating(platform: str):
    return json.loads(elt.qty_by_rating(platforms[platform]))