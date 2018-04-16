SI 206
Final project
Avantika Bagri

Data sources used:
1. News API https://newsapi.org/docs/get-started
		requires API key
		will need to insert API key into secrets.py file

2. CSV databases from https://data.worldbank.org/indicator
		population
		life expectancy
		co2 emissions
		forest area
		country abbreviations

Visuals created:
1. Plotly
		will need to insert username and api_key into secrets.py file

Code structure:
		Some significant functions include:
		1. Getting News data using caching
				getWithCachingNews
				get_news

		2. Creating SQL database
				init_db

		3. Inserting data into database
				insert_csv_data
				insert_json_data
				input_news_data

		4. Using relation key in database to get country abbreviation in each table
				get_country_mapping

		5. Visualization using Plotly
				plotly_population
				plotly_co2
				plotly_forest
				plotly_expectancy

User guide:
		1. Run the final.py file
		2. Ensure that you closely follow the commands and only insert valid country abbreviations and categories
				Sample inputs in <>:
				1. <US sports> will print a list of the most popular news titles and sources
				2. <12> will open the 12th news article in a browser
				3. <graph> will allow you to choose from a variety of data sets
				4. <graph All> will open all four graphs in a browser
				5. <exit> will exit program

Notes:
		1. Ensure you follow command prompts closely when running program
		2. Program and test file may take some time to run -  please be patient!
