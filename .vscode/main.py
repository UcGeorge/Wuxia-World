import os
import requests as req
from bs4 import BeautifulSoup as soup
import json
import re


# GENERAL CONSTANTS
WORKING_DIRECTORY = "F:\\Read Anime\\Light-Novel\\Books\\{}"
WORKING_FILE_DIRECTORY = "F:\\Read Anime\\Light-Novel\\Books\\{}\\{}"
COMMAND_PREFIX = "[WUXIA WORLD] > "
FILE_FORMAT = ".html"
ENCODING = "utf-8"
JSON_DATA = "c:/Users/USER/Wuxia World/.vscode/lib.json"
HTML_PARSE_FORMAT = 'html.parser'
SOURCE = "https://www.wuxiaworld.com{}"
json_data = open(JSON_DATA)
LIBRARY = json.load(json_data)
json_data.close()

# CONSOLE COMMANDS
COMMANDS = ['ADD', 'UPDATE', 'NOVELS', 'EXIT', 'HELP']
EXIT_COMMAND = COMMANDS[3]
LIST_COMMAND = COMMANDS[2]
ADD_COMMAND = COMMANDS[0]
UPDATE_COMMAND = COMMANDS[1]
HELP_COMMANDS = COMMANDS[4]

# JSON DATA KEYS
LATEST_CHAPTER = 'local_latest_chapter'
LATEST_CHAPTER_URL = 'local_latest_chapter_url'

# CONSOLE MESSAGES
NO_UPDATES_MESSAGE = "[NO UPDATES] There were no recent updates beyond {}."
LAST_CHAPTER_MESSAGE = "[LAST CHAPTER] {} is the last chapter."
NEW_CHAPTER_MESSAGE = "[NEW CHAPTER] Getting {}..."
DOWNLOAD_ERROR_MESSAGE = "[DOWNLOAD ERROR] There was an error while trying to get {}"
HTTP_REQUEST_MESSAGE = "[FETCHING DATA] Fetching data from the internet using http requests"
CONNECTION_ERROR_MESSAGE = "[CONNECTION ERROR] There was a problem connecting to DDL"
COMPLETE_MESSAGE = "[SUCCESS] All updates have successfully been downloaded"
LATEST_CHAPTER_MESSAGE = "[LATEST CHAPTER] {} is the last chapter."
NOVEL_MESSAGE = "[UPDATING NOVEL] {}"
COMMAND_ERROR = "[COMMAND ERROR] Your command is invalid!"
EXIT_MESSAGE = "[EXITING] The application is exiting. Goodbye!"
COMMAND_OVERVIEW_MESSAGE = "[COMMAND] Command: {}, Target: {}"
INVALID_LINK = "[INVALID LINK] '{}' does not exist in Wuxia World!"
EMPTY_LIBRARY = "[EMPTY LIBRARY] There are no novels in your library."

# HTML INJECTS
LINK_TEMPLATE = '<a class="inline" href="{}">{}</a>'
BOILER = '''
<html>
    <body>
        <center>
            <div class = "main-content">
                {}
                {}
                <br><hr><br>
                {}
            </div>
            <div>
                {}
            </div>
        </center>
    </body>
    {}
</html>
'''
TITLE = '''
<h1 chass = "main-title">{}</h1>
<h1 chass = "main-title">{}</h1>
'''
PARAGRAPH = '''
<p>
    {}
</p>
'''
STYLE = '''
<style>
        body {
            color: #484848;
            line-height: 1.625;
            background-color : #EEEEEE !important;
        }
        h1 {
            font-size: 35px;
            letter-spacing: 0;
            line-height: 140%;
            font-weight: 600;
            margin-top: 10px;
            margin-right: auto;
            margin-bottom: 10px;
            margin-left: auto;
            font-family: 'Lato',sans-serif;
            text-align: center;
            color: #000000;
        }
        .main-content {
            background-color : #FFFFFF;
            width : 850px;
            padding-top: 25px;
            padding-right: 35px;
            padding-bottom: 25px;
            padding-left: 35px;
            box-shadow: 0 0 15px rgba(0,0,0,.05);
        }
        .main-content p {
            font-size: 20px !important;
            font-family: 'Lato',sans-serif;
            text-align: left;
        }
        p {
            margin-bottom: 1.5em;
            line-height: 28px;
        }
</style>
'''
READER = '''
<!DOCTYPE html>
<html>

<head>
    <title>
        {0}
    </title>
    <link rel="stylesheet" href="style.css">
</head>

<body>

    <div id="mainArea" class="card">
        <div>
            <ul>
                <li class="inline"><button id="9" onclick="incS(9)">
                    <h2>9</h2>
                </button></li>
                <li class="inline"><button id="8" onclick="incS(8)">
                    <h2>8</h2>
                </button></li>
                <li class="inline"><button id="7" onclick="incS(7)">
                    <h2>7</h2>
                </button></li>
                <li class="inline">
                    <button id="add" onclick="inc()">
                        <h2>+</h2>
                    </button>
                </li>
            </ul>
            <ul>
                <li class="inline"><button id="6" onclick="incS(6)">
                    <h2>6</h2>
                </button></li>
                <li class="inline"><button id="5" onclick="incS(5)">
                    <h2>5</h2>
                </button></li>
                <li class="inline"><button id="4" onclick="incS(4)">
                    <h2>4</h2>
                </button></li>
                <li class="inline">
                    <button id="sub" onclick="dec()">
                        <h2>-</h2>
                    </button>
                </li>
            </ul>
            <ul>
                <li class="inline"><button id="3" onclick="incS(3)">
                    <h2>3</h2>
                </button></li>
                <li class="inline"><button id="2" onclick="incS(2)">
                    <h2>2</h2>
                </button></li>
                <li class="inline"><button id="1" onclick="incS(1)">
                    <h2>1</h2>
                </button></li>
                <li class="inline"><button id="0" onclick="incS(0)">
                    <h2>0</h2>
                </button></li>
            </ul>
            <ul>
                <li class="inline"><button id="next_btn" onclick="load()">                       
                        <h2>READ - Ch <span id = 'chapterNum'></span></h2>
                    </button></li>
                <li class="inline"><button id="back" onclick="backspace()">
                    <h2><<</h2>
                </button></li>
            </ul>
        </div>
    </div>
    <script>
        var Book = {{
            tempIndex: '',
            index: 1,
            chapterloc: '{0}/Chapter ',
            chaptersuf: '.html',
        }}
        window.onload = function() {{
            document.getElementById('chapterNum').innerHTML = Book.index;
        }}
        var load = function() {{
            if (Book.tempIndex == '') {{
                var link = Book.chapterloc + Book.index + Book.chaptersuf;
                window.open(link);
                Book.index++;
                document.getElementById('chapterNum').innerHTML = Book.index;
                console.log(link);
            }} else {{
                Book.index = Book.tempIndex;
                var link = Book.chapterloc + Book.tempIndex + Book.chaptersuf;
                window.open(link);
                Book.index++;
                document.getElementById('chapterNum').innerHTML = Book.index;
                Book.tempIndex = '';
            }}
        }}
        var inc = function() {{
            Book.index++;
            document.getElementById('chapterNum').innerHTML = Book.index;
            var link = Book.chapterloc + (Book.index) + Book.chaptersuf;
            console.log(link);
        }}
        var dec = function() {{
            Book.index--;
            document.getElementById('chapterNum').innerHTML = Book.index;
            var link = Book.chapterloc + (Book.index) + Book.chaptersuf;
            console.log(link);
        }}
        var incS = function(a) {{
            Book.tempIndex += a;
            document.getElementById('chapterNum').innerHTML = Book.tempIndex;
        }}

        var backspace = function() {{
            if (Book.tempIndex != '') {{
                Book.tempIndex = Book.tempIndex.slice(0, Book.tempIndex.length - 1);
                document.getElementById('chapterNum').innerHTML = Book.tempIndex;
            }}
        }}
    </script>

</body>

</html>
'''


def get_from_soup(url, novel):
    # print(url)
    try:
        headers = {'User-Agent': 'PostmanRuntime/7.26.5'}
        html = req.get(url, headers=headers).text
        # print(html)
    except:
        print(CONNECTION_ERROR_MESSAGE)
        return (None, None, None)

    _soup = soup(html, HTML_PARSE_FORMAT)

    title = _soup.find(
        "div", {"class": "caption clearfix"}).findAll('div')[-1].text.strip()
    print(f'[FETCHING TITLE] {title}')
    if '(Teaser)' in title:
        raise Exception('LastChapter')

    main = _soup.find("div", {"id": "chapter-content"}).findAll('p')
    title_text = TITLE.format(novel, title)
    main_text = ""

    for stuff in main:
        main_text += PARAGRAPH.format(stuff.text)

    try:
        chapter_num = int(
            re.search(r"\d+", LIBRARY[novel][LATEST_CHAPTER]).group()) + 1
        next_chapter_link = WORKING_FILE_DIRECTORY.format(
            novel, f'Chapter {chapter_num + 1}' + FILE_FORMAT)
        prev_chapter_link = WORKING_FILE_DIRECTORY.format(
            novel, f'Chapter {chapter_num - 1}' + FILE_FORMAT)
        links = LINK_TEMPLATE.format(
            prev_chapter_link, 'Previous') + '--------------------' + LINK_TEMPLATE.format(next_chapter_link, 'Next')
    except KeyError:
        next_clapter_link = WORKING_FILE_DIRECTORY.format(
            novel, 'Chapter 2' + FILE_FORMAT)
        links = LINK_TEMPLATE.format(next_clapter_link, 'Next')

    html_text = BOILER.format(title_text, links, main_text, links, STYLE)

    try:
        next_url = SOURCE.format(_soup.find("li", {"class": "next"}).a['href'])
    except AttributeError:
        raise Exception('InvalidLinkError')

    return (next_url, html_text)


def capital(a):
    stuff = a.split(' ')
    temp = ""

    for b in stuff:
        temp += b[0].upper() + b.lstrip(b[0]) + ' '

    return temp.strip()


def get_updates(novel):
    print(NOVEL_MESSAGE.format(novel))
    last_chapter_url = LIBRARY[novel][LATEST_CHAPTER_URL]
    next_chapter_url, chapter_html = get_from_soup(
        last_chapter_url, novel)

    while next_chapter_url != None:
        chapter_url = next_chapter_url
        try:
            next_chapter_url, chapter_html = get_from_soup(
                chapter_url, novel)
        except:
            print(LAST_CHAPTER_MESSAGE.format(
                LIBRARY[novel][LATEST_CHAPTER]))
            return

        try:
            chapter_num = int(
                re.search(r"\d+", LIBRARY[novel][LATEST_CHAPTER]).group()) + 1
            chapter_name = f'Chapter {chapter_num}'

            with open(WORKING_FILE_DIRECTORY.format(novel, chapter_name + FILE_FORMAT), "w", encoding=ENCODING) as chapter_file:
                chapter_file.write(chapter_html)
            with open(JSON_DATA, "w") as json_file:
                LIBRARY[novel]["local_latest_chapter"] = chapter_name
                LIBRARY[novel]["local_latest_chapter_url"] = chapter_url
                json.dump(LIBRARY, json_file)
                pass
        except:
            print(DOWNLOAD_ERROR_MESSAGE.format(
                LIBRARY[novel][LATEST_CHAPTER]))


def add_novel(novel):
    print(HTTP_REQUEST_MESSAGE)
    link = SOURCE.format('/novel/' + novel.replace(' ', '-'))

    try:
        headers = {'User-Agent': 'PostmanRuntime/7.26.5'}
        html = req.get(link, headers=headers)
    except:
        print(CONNECTION_ERROR_MESSAGE)
        return

    _soup = soup(html.text, HTML_PARSE_FORMAT)

    try:
        if _soup.find("div", {"class": 'panel-heading'}).text == 'Page Not Found':
            print(INVALID_LINK.format(novel))
            return
    except:
        print('link is valid')
        pass

    first_chapter_link = SOURCE.format(_soup.find(
        "li", {"class": 'chapter-item'}).a['href'])

    try:
        next_chapter_url, chapter_html = get_from_soup(
            first_chapter_link, novel)
    except Exception:
        print('[CHAPTER ERROR] The chapters of this novel are not hosted on DDL')
        return

    try:
        os.mkdir(WORKING_DIRECTORY.format(capital(novel)))
        with open(WORKING_FILE_DIRECTORY.format(capital(novel), 'Chapter 1' + FILE_FORMAT), "w", encoding=ENCODING) as chapter_file:
            chapter_file.write(chapter_html)

        with open(WORKING_DIRECTORY.format(capital(novel) + FILE_FORMAT), "w", encoding=ENCODING) as reader_file:
            reader_file.write(READER.format(capital(novel)))

        with open(JSON_DATA, "w") as json_file:
            LIBRARY[novel] = {}
            LIBRARY[novel]["local_latest_chapter"] = "Chapter 1"
            LIBRARY[novel]["local_latest_chapter_url"] = first_chapter_link
            json.dump(LIBRARY, json_file)
    except:
        print(DOWNLOAD_ERROR_MESSAGE.format('Chapter 1'))
        return

    print(f'[SUCCESS] {novel} has been added to your library.')


def help():
    print('[COMMANDS]')
    for command in COMMANDS:
        if command == ADD_COMMAND:
            print("  ADD [novel]- Add [novel] to your library")
        elif command == UPDATE_COMMAND:
            print(
                "  UPDATE [novel]- Update [novel] in your library. Note: [novel] must be in your library.")
        elif command == LIST_COMMAND:
            print("  NOVELS - List the novels in your library.")
        elif command == HELP_COMMANDS:
            print("  HELP - Show help.")
        elif command == EXIT_COMMAND:
            print("  EXIT - Exit application.")


def novels():
    if LIBRARY == {}:
        print(EMPTY_LIBRARY)
        return
    print('[NOVELS]')

    for novel in LIBRARY:
        print('  ', novel)
    pass


while True:
    print('')
    user_input = input(COMMAND_PREFIX).split(' ')
    command = user_input[0].upper()
    target = ''
    try:
        user_input.remove(user_input[0])
        for word in user_input:
            target += (word + ' ')
        target = target.strip().lower()
    except IndexError:
        pass
    except:
        pass

    if command not in COMMANDS:
        print(COMMAND_ERROR)
        continue

    if command == EXIT_COMMAND:
        print(EXIT_MESSAGE)
        print('')
        break

    if command == HELP_COMMANDS:
        help()
        continue

    if command == LIST_COMMAND:
        novels()
        continue

    if command == UPDATE_COMMAND:
        if target not in LIBRARY:
            print(f'[ERROR] "{target}" is not in your library.')
            continue
        get_updates(target)
        continue

    if command == ADD_COMMAND:
        if target in LIBRARY:
            print(f'[ERROR] "{target}" is already in your library.')
            continue
        add_novel(target)
        continue
