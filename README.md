Recent Update (1.4):
Synonyms can be accessed by adding a '~' before a word. Works great, but fair warning, if the word doesn't end with a space (i.e. -> .,!?) -- it's touch and go whether it's recognized as a real word.
Hyponyms and hypernyms can be accessed through the same convention -- however, the activation symbols are obviously different -- '^' and '>' are their access triggers, respectively.

Quick view into the program visually:
https://www.youtube.com/watch?v=DaeklssYOyo

Intro:


DiceWords is a new way to more precisely work with dynamic prompting, and will be occasionally updated and unified with clean, well-created and curated user-contributed material.
If you'd like to help keep software like this free, remember someone has to make it, so consider joining the team. https://discord.gg/v73CFMVnV4




Install instructions:


Update 10/28/23:
An install batch file has been added, in most cases it should take care of everything, and the app will be good to go.


Manual instructions for the unusual case the batch wouldn't work:

Make sure you have Python 3.10+
(3.10.7 or higher should ensure everything works, but 3.10 in general should work)


Open the main DiceWords folder (the highest level of the whole file)

Right click, then select "open in terminal" on that folder area.

Create a python virtual environment
Write:
```
Python -m venv .venv
```
Hit enter.
Then write:
```
.venv\Scripts\activate
```
This will open the new virtual environment.

Then write:
```
pip install -r requirements.txt
```
This will install the dependancies. Then it'll work!

Questions? Discord, ask for @MackNcD, @Gille, or @Note
