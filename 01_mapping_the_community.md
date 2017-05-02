# 01 | Mapping the Community

Gathering lists of Twitter profiles. Filtering users according to their profile descriptions, searching for keywords. Keywords are constantly updated according to results.

## First list of profiles

In order to find interesting enough discourse on Twitter, which is relevant to understanding the relationship between digital tools and architectural design, I started with a short list of users that satisfied the following conditions: the protagonists of this discourse would have to be real people and they should be speaking as themselves rather than in front of companies, institutions or similar entities. To begin with, I  selected eight accounts which returner from a search of Twitter profiles for “architect” and OR|"digital, parametric, computation, data, data-driven”. I selected the accounts that came up at the top of this search and corresponded with three relevance criteria for the research. Relevance criteria are: 1) the user tweets about architectural design and tools in an explicit way; 2) the user mentions the word 'digital' or 'data-driven' or 'parametric' every less than 50 tweets; 3) the users shares opinions; Meeting of these criteria is determined based on my qualitative assessment.

Checked the selected accounts using the [botornot Python API](https://github.com/truthy/botornot-python) to determine their (un)likeliness to be or appear as bots. The smaller the value, the more authentic the tweets of the user appear.

| User | bot or not score |
| -----:| -------------:|
| ProvingGroundIO | 0.56 |
| Parametric01 | 0.26 |
| archinate | 0.4 |
| digitag | 0.55 |
| andydeutsch | 0.63 |
| BjarkeIngels | 0.5 |
| etroxel | 0.18 |
| ColinMcCrone | 0.32 |
| 60secondrevit | 0.37 | *blocked me
| iperezarnal | 0.32 |
| arhitekturality | 0.31 |  (! i am a bot !)

## First keyword list

By carefully observing the tweets from this collection, with the help of a visual word frequency representation (a wordcloud), I selected the first list of keywords which are relevant to the discourse and which are unambiguously used by the community.

```
LIST FROM A4
```


```
keywords = ['BIM', 'DynamoBIM', 'Revit', 'AutoCAD', 'Autodesk', 'Rhinoceros 3D', 'Grasshopper 3D', 'Rhino 3D', 'CAAD', 'computer-aided', 'data-driven', 'model-based', '3dprint', 'parametric', 'parametricism',  'parametricist']
```

## Keywords vs Profiles

word ambiguity is reduced when listening to profiles, because the community of architects mostly means architecture in the sense of buildings and not computer hardware. 
