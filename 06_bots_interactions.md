# Report on Twitter activity, July 2017 (MQ residency)

## 6 bots
 - @active_form based on Keller Easterling's Active Form (book Extrastatecraft) https://twitter.com/active_form
 - @contagiousarchi based on Luciana Parisi's Contagious Architecture (book Contagious Architecture) https://twitter.com/contagiousarchi
 - @infosabundance based on Malcolm McCullough's Information Superabundance (book Ambient Architecture) https://twitter.com/infosabundance
 - @digitalimmanent based on Alexander Galoway's concept of Immanence of the Digital (book Laruelle: Against the Digital) https://twitter.com/digitalimmanent
 - @digittools based on Branko Kolarevic's Digital Tools (book Beyond Performativity) https://twitter.com/digittools
 - @a__stack based on Benjamin Bratton's concept of the Stack (book Stack) https://twitter.com/a__stack

### Saturday 08.07.2017
all 6 bots running from Saturday, 08. July at 7PM (@active_form and @contagiousarchi were active earlier, end of May; @digittools came in only at 1AM on Sunday 09. July) until Sunday, 09. July at 10:30
They use the compound markovify model to generate tweets, combining the text from the author with the collection of tweets streamed from profiles. Because author's texts are of different lengths, different emphasis was given to them in the model (see wordcount-emphasis.ods)

### Sunday 09.07.2017
The bots now mention each other randomly, using the mention() function, which randomly selects one of the 5 remaining bots, or an empty string, and adds it to the tweet
from Sunday 09. July at 17:10 to ???

### Monday 10.07.2017
Changed the state size to 1 in generation of the models. Running all 6 bots from 1PM.
