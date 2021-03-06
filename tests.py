import unittest
import final
import sqlite3
from requests_oauthlib import OAuth1
import json
import requests
import secrets
import webbrowser
import csv
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go

news_api_key = secrets.NEWS_API_KEY
twitter_consumer_key = secrets.TWITTER_CONSUMER_KEY
twitter_consumer_secret = secrets.TWITTER_CONSUMER_SECRET
twitter_access_token = secrets.TWITTER_ACCESS_KEY
twitter_access_secret = secrets.TWITTER_ACCESS_SECRET

DBNAME = 'Avantika_Final_206.db'
EXPECTANCYCSV = 'life_expectancy.csv'
POPULATIONCSV = 'population.csv'
CO2CSV = 'co2_emission.csv'
FORESTCSV = 'forest_area.csv'
COUNTRIESJSON = 'countries.json'

# on startup, try to load the cache from file
CACHE_NEWS = 'cache_news.json'
try:
    cache_file = open(CACHE_NEWS, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION_NEWS = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION_NEWS = {}

def getWithCachingNews(actualURL):
    #actualURL = baseURL + "?" + "country" + "=" + country_abbr + "&" + "category" + "=" + specific_category + "&" + "apiKey" + "=" + news_api_key
    #print(actualURL)
    if actualURL in CACHE_DICTION_NEWS:
        #print("Getting data from cache")
        return CACHE_DICTION_NEWS[actualURL]
    else:

    #if actualURL not in CACHE_DICTION_NEWS:
        #print ("Getting data from API")
        reply = requests.get(actualURL)
        replyjson = reply.text
        CACHE_DICTION_NEWS[actualURL] = json.loads(replyjson)

        cached = open(CACHE_NEWS, 'w')
        cached.write(json.dumps(CACHE_DICTION_NEWS, indent = 2))
        #print(cached)
        cached.close()
    #else:
        #print ("Getting data from cache")
        return CACHE_DICTION_NEWS[actualURL]

#Code for getting news data
def get_news(country_abbr, specific_category):
    #country_abbr = ''
    #specific_category = ''
    baseURL = 'https://newsapi.org/v2/top-headlines'
    #param = {'country': country_abbr, 'category': specific_category, 'apiKey': news_api_key}
    actualURL = baseURL + "?" + "country" + "=" + country_abbr + "&" + "category" + "=" + specific_category + "&" + "pageSize" + "=" + "100" + "&" + "apiKey" + "=" + news_api_key
    #print(actualURL)
    #news = getWithCachingNews(base, params = param)
    news = getWithCachingNews(actualURL)
    #print(news)
    return news

#create database
def init_db():
    #print('Creating Database.')
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    # Drop table if already exists
    statement_e = '''
        DROP TABLE IF EXISTS 'LifeExpectancy';
    '''
    cur.execute(statement_e)
    conn.commit()

    statement_expectancy = '''
        CREATE TABLE 'LifeExpectancy' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'CountryName' TEXT NOT NULL,
            'CountryCode2' TEXT NOT NULL,
            'CountryCode3' TEXT NOT NULL,
            'Exp1960' INTEGER,
            'Exp1980' INTEGER,
            'Exp2000' INTEGER,
            'Exp2015' INTEGER
        );
    '''
    cur.execute(statement_expectancy)
    conn.commit()
    # Drop table if already exists
    statement_p = '''
        DROP TABLE IF EXISTS 'Population';
    '''
    cur.execute(statement_p)
    conn.commit()

    statement_population = '''
        CREATE TABLE 'Population' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'CountryName' TEXT NOT NULL,
            'CountryCode2' TEXT NOT NULL,
            'CountryCode3' TEXT NOT NULL,
            'Pop1960' INTEGER,
            'Pop1980' INTEGER,
            'Pop2000' INTEGER,
            'Pop2015' INTEGER
        );
    '''
    cur.execute(statement_population)
    conn.commit()
    # Drop table if already exists
    statement_co = '''
        DROP TABLE IF EXISTS 'CO2Emission';
    '''
    cur.execute(statement_co)
    conn.commit()

    statement_co2emission = '''
        CREATE TABLE 'CO2Emission' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'CountryName' TEXT NOT NULL,
            'CountryCode2' TEXT NOT NULL,
            'CountryCode3' TEXT NOT NULL,
            'CO1960' INTEGER,
            'CO1980' INTEGER,
            'CO2000' INTEGER,
            'CO2014' INTEGER
        );
    '''
    cur.execute(statement_co2emission)
    conn.commit()

    # Drop table if already exists
    statement_f = '''
        DROP TABLE IF EXISTS 'ForestArea';
    '''
    cur.execute(statement_f)
    conn.commit()

    statement_forest = '''
        CREATE TABLE 'ForestArea' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'CountryName' TEXT NOT NULL,
            'CountryCode2' TEXT NOT NULL,
            'CountryCode3' TEXT NOT NULL,
            'For1990' INTEGER,
            'For2000' INTEGER,
            'For2010' INTEGER,
            'For2015' INTEGER
        );
    '''
    cur.execute(statement_forest)
    conn.commit()

    # Drop table if already exists
    statement_c = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement_c)
    conn.commit()

    statement_countries = '''
        CREATE TABLE 'Countries' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' TEXT NOT NULL,
            'Alpha3' TEXT NOT NULL,
            'CountryName' TEXT NOT NULL
        );
    '''
    cur.execute(statement_countries)
    conn.commit()
    # Drop table if already exists
    statement_n = '''
        DROP TABLE IF EXISTS 'News';
    '''
    cur.execute(statement_n)
    conn.commit()

    statement_news = '''
        CREATE TABLE 'News' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'SourceName' TEXT,
            'Author' TEXT,
            'Title' TEXT,
            'Description' TEXT,
            'URL' TEXT,
            'PublishDate' TEXT,
            'Country' TEXT,
            'Category' TEXT
        );
    '''
    cur.execute(statement_news)
    conn.commit()
    conn.close()

#insert csv data
def insert_csv_data():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    with open(EXPECTANCYCSV,  encoding = 'utf8') as csvExpectancyDataFile:
        csvExpectancyReader = csv.reader(csvExpectancyDataFile)
        next(csvExpectancyReader, None)  # skip the headers

        for row in csvExpectancyReader:
            countryId= ""
            #origin =""
            #cocoa = row[4][:-1]
            insertion = (None, row[0], countryId, row[1], row[4].split('.')[0], row[24].split('.')[0], row[44].split('.')[0], row[59].split('.')[0])
            statement = 'INSERT INTO "LifeExpectancy" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()

    with open(POPULATIONCSV,  encoding = 'utf8') as csvPopulationDataFile:
        csvPopulationReader = csv.reader(csvPopulationDataFile)
        next(csvPopulationReader, None)  # skip the headers

        for row in csvPopulationReader:
            countryId= ""
            #origin =""
            #cocoa = row[4][:-1]
            insertion = (None, row[0], countryId, row[1], row[4].split('.')[0], row[24].split('.')[0], row[44].split('.')[0], row[59].split('.')[0])
            statement = 'INSERT INTO "Population" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()

    with open(CO2CSV,  encoding = 'utf8') as csvCO2DataFile:
        csvCO2Reader = csv.reader(csvCO2DataFile)
        next(csvCO2Reader, None)  # skip the headers


        for row in csvCO2Reader:
            countryId= ""
            #origin =""
            #cocoa = row[4][:-1]
            insertion = (None, row[0], countryId, row[1], row[4].split('.')[0], row[24].split('.')[0], row[44].split('.')[0], row[58].split('.')[0])
            statement = 'INSERT INTO "CO2Emission" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()

    with open(FORESTCSV,  encoding = 'utf8') as csvForestDataFile:
        csvForestReader = csv.reader(csvForestDataFile)
        next(csvForestReader, None)  # skip the headers

        for row in csvForestReader:
            #print(row)
            countryId= ""
            #origin =""
            #cocoa = row[4][:-1]
            insertion = (None, row[0], countryId, row[1], row[34].split('.')[0], row[44].split('.')[0], row[54].split('.')[0], row[59].split('.')[0])
            statement = 'INSERT INTO "ForestArea" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()
    conn.close()

def insert_json_data():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    #print('Inserting Data.')
    #with open() as CountriesJSON:
    countriesData = open(COUNTRIESJSON,'r', encoding = 'utf8')
    countriesInfo = countriesData.read()
    countriesObject = json.loads(countriesInfo)
    #print(countriesObject)

    for x in countriesObject:
        insertion = (None, x['alpha2Code'], x['alpha3Code'], x['name'])
        #print(insertion)
        statement = 'INSERT INTO "Countries" '
        statement += 'VALUES (?,?,?,?) '
        cur.execute(statement, insertion)
        conn.commit()
    conn.close()

def get_country_mapping():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = 'SELECT * FROM Countries'
    cur.execute(statement)
    country_mapping = {}

    for country in cur:
        country_id = country[1]
        name = country[3]
        country_mapping[name] = country_id
    conn.commit()

    for x in country_mapping:
        country = x
        id = country_mapping[x]
        insert = (id, country)
        statement = 'UPDATE LifeExpectancy '
        statement += 'SET CountryCode2 =? '
        statement += 'WHERE CountryName =?'
        cur.execute(statement,insert)

        us_statement = 'UPDATE LifeExpectancy SET CountryCode2 = "US" WHERE CountryName = "United States"'
        cur.execute(us_statement)

        egypt_statement = 'UPDATE LifeExpectancy SET CountryCode2 = "EG" WHERE CountryName = "Egypt, Arab Rep."'
        cur.execute(egypt_statement)

        venezuela_statement = 'UPDATE LifeExpectancy SET CountryCode2 = "VE" WHERE CountryName = "Venezuela, RB"'
        cur.execute(venezuela_statement)
        conn.commit()

    for x in country_mapping:
        country = x
        id = country_mapping[x]
        insert = (id, country)
        statement = 'UPDATE Population '
        statement += 'SET CountryCode2 =? '
        statement += 'WHERE CountryName =?'
        cur.execute(statement,insert)

        us_statement = 'UPDATE Population SET CountryCode2 = "US" WHERE CountryName ="United States"'
        cur.execute(us_statement)

        egypt_statement = 'UPDATE Population SET CountryCode2 = "EG" WHERE CountryName = "Egypt, Arab Rep."'
        cur.execute(egypt_statement)

        venezuela_statement = 'UPDATE Population SET CountryCode2 = "VE" WHERE CountryName = "Venezuela, RB"'
        cur.execute(venezuela_statement)

        conn.commit()

    for x in country_mapping:
        country = x
        id = country_mapping[x]
        insert = (id, country)
        statement = 'UPDATE CO2Emission '
        statement += 'SET CountryCode2 =? '
        statement += 'WHERE CountryName =?'
        cur.execute(statement,insert)

        us_statement = 'UPDATE CO2Emission SET CountryCode2 = "US" WHERE CountryName ="United States"'
        cur.execute(us_statement)

        egypt_statement = 'UPDATE CO2Emission SET CountryCode2 = "EG" WHERE CountryName = "Egypt, Arab Rep."'
        cur.execute(egypt_statement)

        venezuela_statement = 'UPDATE CO2Emission SET CountryCode2 = "VE" WHERE CountryName = "Venezuela, RB"'
        cur.execute(venezuela_statement)

        conn.commit()

    for x in country_mapping:
        country = x
        id = country_mapping[x]
        insert = (id, country)
        statement = 'UPDATE ForestArea '
        statement += 'SET CountryCode2 =? '
        statement += 'WHERE CountryName =?'
        cur.execute(statement,insert)

        us_statement = 'UPDATE ForestArea SET CountryCode2 = "US" WHERE CountryName ="United States"'
        cur.execute(us_statement)

        egypt_statement = 'UPDATE ForestArea SET CountryCode2 = "EG" WHERE CountryName = "Egypt, Arab Rep."'
        cur.execute(egypt_statement)

        venezuela_statement = 'UPDATE ForestArea SET CountryCode2 = "VE" WHERE CountryName = "Venezuela, RB"'
        cur.execute(venezuela_statement)

        conn.commit()
    conn.close()

def input_news_data(country_abbr, specific_category):

    #get data
    data = get_news(country_abbr, specific_category)
    keys = []
    for key in data:
        keys += [key]
    #print(keys)

    #finding number of different commands in cache
    num = 0
    numbers = []
    for url in keys:
        num += 1
        numbers += [num]
    #print(numbers)

    #adding all commands to a list
    all_articles = data['articles']
    # for x in numbers:
    #     articles = data[keys[x-1]]['articles']
    #     all_articles += articles

    all_info_list = []
    for article in all_articles:
        sourcename =  article['source']['name']
        author = article['author']
        title = article['title']
        description = article['description']
        url = article['url']
        date = article['publishedAt']
        dict = {'SourceName':sourcename, 'Author':author, 'Title':title, 'Description':description, 'URL': url, 'PublishDate':date, 'Abbr':country_abbr, 'category':specific_category}
        all_info_list += [dict]

    #print(all_info_list)
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    #print('Inserting Data.')
    for x in all_info_list:
        insertion = (None, x['SourceName'], x['Author'], x['Title'], x['Description'], x['URL'], x['PublishDate'],x['Abbr'],x['category'])
        #print(insertion)
        statement = 'INSERT INTO "News" '
        statement += 'VALUES (?,?,?,?,?,?,?,?,?) '
        cur.execute(statement, insertion)
        conn.commit()
    conn.close()


def news_statements():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    news_results = []
    news_query = "SELECT News.SourceName, News.Title, News.Description, News.URL FROM News "
    cur.execute(news_query)

    for row in cur:
        sourcename = row[0]
        title = row[1]
        description = row[2]
        url = row[3]
        article = [sourcename,title,description,url]
        news_results.append(article)
    return news_results

def plotly_population(country_abbr):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    population_results = []
    population_query = "SELECT Population.Pop1960,Population.Pop1980,Population.Pop2000,Population.Pop2015 FROM Population "
    population_query += "WHERE CountryCode2 = '{}'".format(country_abbr)
    cur.execute(population_query)

    for row in cur:
        p1 = int(row[0])
        p2 = int(row[1])
        p3 = int(row[2])
        p4 = int(row[3])
        population_results = [p1,p2,p3,p4]

    #print(population_results)

    year = ['1960','1980', '2000', '2015']
    data = [population_results[0],population_results[1],population_results[2],population_results[3]]
    #data = [8996351, 13248370, 20093756, 33736494] #input from database

    #create and style traces
    trace = go.Scatter(
        x = year,
        y = data,
        name = 'Population Data for ' + country_abbr,
        line = dict(
            color = ('rgb(205,12,24)'),
            width = 4)
        )
    data = [trace]
    title = 'Population Data ' + country_abbr
    #edit layout
    layout = dict(title = title, xaxis = dict(title = 'Year'), yaxis = dict(title = 'Population (in 1000s)'))

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'pop-styled-line')

def plotly_expectancy(country_abbr):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    expectancy_results = []
    expectancy_query = "SELECT LifeExpectancy.Exp1960,LifeExpectancy.Exp1980,LifeExpectancy.Exp2000,LifeExpectancy.Exp2015 FROM LifeExpectancy "
    expectancy_query += "WHERE CountryCode2 = '{}'".format(country_abbr)
    cur.execute(expectancy_query)

    for row in cur:
        e1 = int(row[0])
        e2 = int(row[1])
        e3 = int(row[2])
        e4 = int(row[3])
        expectancy_results = [e1,e2,e3,e4]

    year = ['1960','1980', '2000', '2015']
    data = [expectancy_results[0],expectancy_results[1],expectancy_results[2],expectancy_results[3]]

    #create and style traces
    trace = go.Scatter(
        x = year,
        y = data,
        name = 'Life Expectancy Data for ' + country_abbr,
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4)
        )
    data = [trace]
    #edit layout
    layout = dict(title = 'Life Expectancy', xaxis = dict(title = 'Year'), yaxis = dict(title = 'Age (years)'))

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'exp-styled-line')

def plotly_co2(country_abbr):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    co2_results = []
    co2_query = "SELECT CO2Emission.CO1960,CO2Emission.CO1980,CO2Emission.CO2000,CO2Emission.CO2014 FROM CO2Emission "
    co2_query += "WHERE CountryCode2 = '{}'".format(country_abbr)
    cur.execute(co2_query)

    for row in cur:
        c1 = int(row[0])
        c2 = int(row[1])
        c3 = int(row[2])
        c4 = int(row[3])
        co2_results = [c1,c2,c3,c4]

    year = ['1960','1980', '2000', '2014']
    data = [co2_results[0],co2_results[1],co2_results[2],co2_results[3]]

    #create and style traces
    trace = go.Scatter(
        x = year,
        y = data,
        name = 'CO2 Emission Data for ' + country_abbr,
        line = dict(
            color = ('rgb(143, 19, 131)'),
            width = 4)
        )
    data = [trace]
    #edit layout
    layout = dict(title = 'CO2 Emission Data', xaxis = dict(title = 'Year'), yaxis = dict(title = 'KT (million)'))

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'co2-styled-line')

def plotly_forest(country_abbr):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    forest_results = []
    forest_query = "SELECT ForestArea.For2000,ForestArea.For2010,ForestArea.For2015 FROM ForestArea "
    forest_query += "WHERE CountryCode2 = '{}'".format(country_abbr)
    cur.execute(forest_query)

    for row in cur:
        f1 = row[0]
        f2 = row[1]
        f3 = row[2]
        forest_results = [f1,f2,f3]

    year = ['1990','2000', '2010', '2015']
    data = [forest_results[0],forest_results[1],forest_results[2]]

    #create and style traces
    trace = go.Scatter(
        x = year,
        y = data,
        name = 'Forest Area Data for ' + country_abbr,
        line = dict(
            color = ('rgb(91, 143, 19)'),
            width = 4)
        )
    data = [trace]
    #edit layout
    layout = dict(title = 'Forest Area', xaxis = dict(title = 'Year'), yaxis = dict(title = '(%) of Land'))

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'forest-styled-line')

def call_functions(country_abbr,specific_category):
    init_db()
    insert_csv_data()
    insert_json_data()
    get_country_mapping()
    input_news_data(country_abbr,specific_category)
    news_statements()


class Test(unittest.TestCase):
    final.init_db()
    final.insert_csv_data()
    final.insert_json_data()
    final.get_country_mapping()
    final.input_news_data('US','technology')

    def test_population(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        population_results = []
        population_query = "SELECT Population.Pop1960,Population.Pop1980,Population.Pop2000,Population.Pop2015 FROM Population "
        population_query += "WHERE CountryCode2 = '{}'".format('TH')
        cur.execute(population_query)

        for row in cur:
            p1 = int(row[0])
            p2 = int(row[1])
            p3 = int(row[2])
            p4 = int(row[3])
            population_results = [p1,p2,p3,p4]
        self.assertEqual(p1,27397175)
        self.assertEqual(p2,47385323)
        self.assertEqual(p3,62958021)
        self.assertEqual(p4,68657600)

    def test_expectancy(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        expectancy_results = []
        expectancy_query = "SELECT LifeExpectancy.Exp1960,LifeExpectancy.Exp1980,LifeExpectancy.Exp2000,LifeExpectancy.Exp2015 FROM LifeExpectancy "
        expectancy_query += "WHERE CountryCode2 = '{}'".format('US')
        cur.execute(expectancy_query)
        for row in cur:
            e1 = int(row[0])
            e2 = int(row[1])
            e3 = int(row[2])
            e4 = int(row[3])
            expectancy_results = [e1,e2,e3,e4]
        self.assertEqual(e1,69)
        self.assertEqual(e2,73)
        self.assertEqual(e3,76)
        self.assertEqual(e4,78)

    def test_co2(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        co2_results = []
        co2_query = "SELECT CO2Emission.CO1960,CO2Emission.CO1980,CO2Emission.CO2000,CO2Emission.CO2014 FROM CO2Emission "
        co2_query += "WHERE CountryCode2 = '{}'".format('IN')
        cur.execute(co2_query)

        for row in cur:
            c1 = int(row[0])
            c2 = int(row[1])
            c3 = int(row[2])
            c4 = int(row[3])
            co2_results = [c1,c2,c3,c4]
        self.assertEqual(c1,120581)
        self.assertEqual(c2,314016)
        self.assertEqual(c3,1031853)
        self.assertEqual(c4,2238377)

    def test_forest(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        forest_results = []
        forest_query = "SELECT ForestArea.For2000,ForestArea.For2010,ForestArea.For2015 FROM ForestArea "
        forest_query += "WHERE CountryCode2 = '{}'".format('BR')
        cur.execute(forest_query)

        for row in cur:
            f1 = row[0]
            f2 = row[1]
            f3 = row[2]
            forest_results = [f1,f2,f3]
        self.assertEqual(f1,62)
        self.assertEqual(f2,59)
        self.assertEqual(f3,59)

if __name__ == "__main__":
	unittest.main(verbosity=2)
