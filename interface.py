import pandas as pd

#Reading datasets
df_a=pd.read_csv('Datasets/amazon_prime_titles-score.csv') #amazon
df_d=pd.read_csv('Datasets/disney_plus_titles-score.csv') #disney
df_h=pd.read_csv('Datasets/hulu_titles-score (2).csv') #hulu
df_n=pd.read_csv('Datasets/netflix_titles-score.csv') #netflix

#Functions
def transform(input_dataframe, idx_char):
    df=input_dataframe
    df.loc[:,['show_id']]=idx_char+df.loc[:,['show_id']] #Modifying id
    df['rating'].fillna('G', inplace=True) #Replace NAs
    df['date_added']=df.date_added.str.strip() #Remove blank spaces at start (netflix problem)
    df['date_added']=pd.to_datetime(df['date_added'], format='%B %d, %Y') #Convert dates
    df[['duration_int', 'duration_type']]=df.duration.str.split(" ", expand=True) #Splitting in duration_int & duration_type
    df['duration_type']=df['duration_type'].replace(['Seasons', 'Season'], 'season') #Normalization of duration_type
    return df

def findby_keyword(input_dataframe, keyword): #Number of times of 'keyword' in 'title' of input_dataframe
    df=input_dataframe
    rows=len(df[df['title'].str.contains(str.capitalize(keyword))])
    return {'keyword': keyword, 'quantity': rows} # /api/{platform}/{keyword}

def findby_score_per_year(input_dataframe, year, score): #Number of movies in year with score >= value
    df=input_dataframe
    rows=len(df[(df['date_added'].dt.year==year) & (df['score']>=score)])
    return {'year':year, 'score': score, 'quantity':rows} # /api/{platform}/{year}/{score}

def find_second_max_score(input_dataframe): #Second movie with max 'score'
    df=input_dataframe
    return df[df['score']==df['score'].max()].sort_values(by=['title']).iloc[1].to_json() # /api/2nd_max_score/{platform}

def findby_max_duration(input_dataframe, duration_type): #Movie with max duration according to type (min|season)
    df=input_dataframe
    return df[df['duration_type']==duration_type].sort_values(by=['duration_int']).iloc[-1].to_json() # /api/max_duration/{platform}/{duration_type}

def qty_by_rating(input_dataframe): #Qty of series/movies by rating
    df=input_dataframe
    return df['rating'].value_counts().to_json() # /api/qty_by_rating/{platform}

#Transformed datasets
amazon=transform(df_a,'a')
disney=transform(df_d, 'd')
hulu=transform(df_h, 'h')
netflix=transform(df_n, 'n')