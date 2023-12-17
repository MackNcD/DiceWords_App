Recent Update (1.4):
Synonyms can be accessed by adding a '~' before a word. Works great, but fair warning, if the word doesn't end with a space (i.e. -> .,!?) -- it's touch and go whether it's recognized as a real word.
Hyponyms and hypernyms can be accessed through the same convention -- however, the activation symbols are obviously different -- '^' and '>' are their access triggers, respectively.
Python is being a ***** about highlighting these new forms of dynamic input, if it bugs people that the words don't change color like they do for DiceWords themselves, I'll find a way.

Intro:

DiceWords is a new way to more precisely work with dynamic prompting, and will be continuously updated and continuously unified with clean, well-created and curated user-contributed material.
If you'd like to help keep software like this free, please consider contributing a few cents. https://www.buymeacoffee.com/dicewords

Another great way to keep the gates of open source open, is to give back, you can find/share DiceWords on our discord. 
The discord is also a place for new developers who are looking to get in on projects surround LLMs & Image Generation and other creative applicaions of AI.
We also want to hear your ideas of how to make this program phenomenal, your ideas for new projects, and your thoughts on the current flock of WIPs. The current new projects under wraps will dwarf this one. You can reach us on Discord, we don't bite (except for Austin, who goes by "Note" on Discord, PM him and tell him to stop biting):
https://discord.gg/v73CFMVnV4

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

Python -m venv .venv

Hit enter.
Then write:

.venv\Scripts\activate

This will open the new virtual environment.

Then write:
pip install -r requirements.txt

This will install the dependancies. Then you can open main.py and run it in windows studio code.

Ask for @Note, @MackNcD, or @Gille

EDIT: There's doubles of the shapes files
