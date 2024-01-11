## OpenRussian to Anki Scraper

# About
OpenRussian to Anki Scraper is a scraper for the website [OpenRussian](https://openrussian.org/). It is a personal project for the purpose of taking Russian word data from [OpenRussian's language level word list](https://openrussian.org/vocab/A1) and converting it into a .csv file that can then be imported into the program [Anki](https://apps.ankiweb.net/). The scraper makes requests to OpenRussian's api and formats that data to fill several fields in an Anki card.
These include:
- Russian word (front of card)
- Translations (back of card)
- Part of speech (including aspect if applicable)
- Russian example sentence
- English translation of the Russian example sentence
- Pronunciation of the word (Accented Russian word)
- Source URL

# Setup
In order to run this script you must have python version 3.10 or newer (preferably the latest version) installed on your computer. This project does not require any external packages.

# Usage
In the ``scraper.py`` file, there is are a set of preferences for you to adjust. The first and most important is a variable called ``languagelevel``. This variable accepts any of the possible language levels that OpenRussian has a list of words for.
The accepted levels are as follows:
- A1
- A2
- B1
- B2
- C1
- C2

Those familiar with language learning will know these follow the same standard of language proficiency levels outlined by the [Common European Framework of Reference for Languages](https://wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages).

Directly beneath ``languagelevel`` are two variables called ``singletranslationlimit`` and ``uniquetranslationlimit``. ``singletranslationlimit`` refers to the number of translations for a single meaning will be scraped. ``uniquetranslationlimit`` refers to the number of unique meanings will be scraped. Without these limits, some words have many esoteric meanings and can clutter up Anki cards.

The final preference is a variable called ``prependto``. When true, this variable will prepend "to" to any verb's translation if it does not already have it. This can sometimes create strange translations, so it is kept false by default.

Once the desired preferences have been set, simply run the command ``python ./scraper.py`` in the terminal while inside the folder. The terminal will output each word that it has scraped and added to the .csv file it has created. Once it has finished, you can find a new file created following the format ``output1.csv``. This file can then be dragged and imported into Anki, making sure to set the field separator to ``Comma``. You can then set the field mapping according to the card type you prefer to use. Once you are finished and have pressed ``Import``, make sure to go into the browse menu and delete the card with the default data "word", "translations", "part of speech", etc. You are now ready to study Russian in Anki!

It is important to be aware that OpenRussian is a dictionary created and maintained by a community of Russian speakers and learners. Not every translation will be completely accurate or very helpful. This scraper also is not perfect and may miss some meanings of a word or create confusing cards. As a result of these two factors, the quality of every card may not be perfect or even very good. It is important to check each card as you study it and adjust it to be more refined and accurate.

# License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>