# Hypothetizing questions

This process is lead by a quest to formulate questions, rather than find possible answers. In order to allow for questions to emerge from data, we use the process we term "hypothesizing" which describes an observation of importance of certain terms through the measure of their appearance in scientific writing (something we consider documented in goodle n-gram project)

## N-grams for the initial list of keywords
This list of keywords is used to gather tweets in the keyword-based collection process. It is also used to identify profiles to stream.

We look at the books published since 1960 (there is little mention of the terms from the list prior to 1960 and their meaning might have changed too)

First, we explore keywords used in twitter streaming search, also used to identify accounts to follow. Some of these words do not appear in google n-gram data (DynamoBIM, Rhinoceros 3D, Rhino 3D, Grasshopper 3D).

`keywords = ['BIM', 'DynamoBIM', 'Revit', 'AutoCAD', 'Autodesk', 'Rhinoceros 3D', 'Grasshopper 3D', 'Rhino 3D', 'CAAD', 'computer-aided', 'data-driven', 'model-based', '3dprint', 'parametric', 'parametricism',  'parametricist', 'IoT', 'iot', 'sensor', 'network']`

![keywords-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyVzhyZGpXWldKeXc "Keywords n-grams from 1960 to today")

CAD and BIM show interesting trends.

![CAD-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyYVpndi1DeUN5LW8 "Computer-aided * n-grams from 1960 to today")

![BIM-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyYUhkdGFkRWpMSkk "BIM n-gram from 1960 to today")

Also, Internet of Things!

We then look at trends in data-driven and agent-based approaches:

![agent-based-ALL-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyMTRHbDRsYkVLdWc "Agent-based * n-grams from 1960 to today")

![agent-based-4w-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyWVVMWTlTZXY4Snc "Four most significant 'agent-based' n-grams from 1960 to today")

![data-driven-ALL-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyMVVxeDQyVnl1eWM "Data-driven * n-grams from 1960 to today")

![data-driven-4w-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyZTNTQlpDcGEzRzQ "Four most significant 'data-driven' n-grams from 1960 to today")

Comparison between data-driven and agent-based

![agent-based_data-driven-1960-today](https://drive.google.com/uc?id=0B7ptyl0pGIJyd2RYRjhZU3ljX0k "'data driven' vs 'agent-based' n-grams from 1960 to today")

## Word and n-gram frequency in tweets; Comparing to google n-grams

The tweets collection is made of 166,580 words in total. We consider 72577 to be meaningful words, out of which 10213 are unique (14%) and in which #hastags and @mentions make over 25% percent.

![words_profiles-tweets](https://drive.google.com/uc?id=0B7ptyl0pGIJydGNxR3NiLUVJX2c "Analysing tweets from followed profiles, March-August 2017: all the words")

### Most frequent words in the collection of tweets, March-August 2017

![words_profiles-tweets](https://drive.google.com/uc?id=0B7ptyl0pGIJyVnpkQ0ctajhWVTg "Analysing tweets from followed profiles, March-August 2017: most frequent words")

### Most frequent words in the collection of tweets, according to Google n-grams

![words_profiles-google](https://drive.google.com/uc?id=0B7ptyl0pGIJySWdhSzlEX1hzUG8 "Google n-gram for most frequent words in tweets; 1960 until today")

![words_profiles-google](https://drive.google.com/uc?id=0B7ptyl0pGIJyT2wxdThMbUhVWGM "Google n-gram for most frequent words in tweets; 1800 until today")

### Some words popularity stand out. For example, *house* and *model* in Google n-grams:

![model-house-google](https://drive.google.com/uc?id=0B7ptyl0pGIJyTm56NEpmdWlVS0k "Google n-gram for 'house' and 'model'; 1800 until today")

In the collection of tweets, they appear like this:

![model-house-tweets](https://drive.google.com/uc?id=0B7ptyl0pGIJyM3VKZUZZa0V2WG8 "Word frequency for 'house' and 'model' in tweets")

### The other interesting curve is for *design*, *project* and *build*:

![design-project-build-google](https://drive.google.com/uc?id=0B7ptyl0pGIJyOVVDZ2lxdkRJZUU "Google n-gram for 'design', 'project' and 'build'; 1800 until today")

![design-project-build-tweets](https://drive.google.com/uc?id=0B7ptyl0pGIJycnVRMzQ2cURTVnc "Word frequency for 'design', 'project' and 'build' in tweets")

## Textmining the bots

We download all the tweets from the bots. The same word frequency analysis applied to the tweets give the following results (per bot)
