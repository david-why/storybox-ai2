# magic-box.png attribution: <a href="https://www.flaticon.com/free-icons/magic-box" title="magic box icons">Magic box icons created by smashingstocks - Flaticon</a>

import json
import random
import time

from py2ai.components import *  # type: ignore
from py2ai.enums import *  # type: ignore
from py2ai.magic import *  # type: ignore

# region components
# Initialize non-visible components
Screen1 = Form(
    ScreenOrientation='portrait',
    Icon='icon.png',
    Title='Story Box',
    AlignHorizontal=3,
    Theme='AppTheme.Light.DarkActionBar',
    AboutScreen='Create stories for small children with the power of ChatGPT!\n\n'
    'Click "New story" to write a new story. You can specify the style, theme, and '
    'main character of the story. If you don\'t want to type, click the "circle" '
    'button to randomize. Then, click "Write story" to get going!\n\n'
    'Once you have created a story or two, you can browse the stories you wrote by '
    'clicking on the "Hi-story" button from the home page.\n\n'
    'Image credits:\n'
    'Magic box icons created by smashingstocks - Flaticon '
    '(https://www.flaticon.com/free-icons/magic-box)\n\n'
    'App author: David Wang (david-why)\n'
    'Created with py2ai',
    VersionCode=111,
    VersionName='1.1.1',
)
WriterBot = ChatBot(
    Token=CHATBOT_TOKEN,  # type: ignore
    System='You are a story bot that writes stories for children. Use simple '
    'words and sentences. Be creative. Follow the requirements. If the '
    'main character is well known, stay close to the original story.',
)
DeleteNotifier = Notifier()
Notifier1 = Notifier()
TinyDB1 = TinyDB(Namespace='StoryBox')
TextToSpeech1 = TextToSpeech(Language='en', Country='USA')
Sharing1 = Sharing()
StoryClock = Clock(TimerInterval=1, TimerEnabled=False)

# region scope1
# First "screen": The home page with beeg image
Scope1 = VerticalArrangement(Width=-1095, Height=-2, AlignHorizontal=3)
Spacing1 = VerticalArrangement(parent=Scope1, Height=-1005)
MagicImage = Image(parent=Scope1, Height=-1050, Picture='magic-box.png')
Spacing12 = VerticalArrangement(parent=Scope1, Height=-1005)
StartButton = Button(
    parent=Scope1,
    FontSize=24,
    Text='🗒️ New story',
    BackgroundColor='&HFF66CC66',
    Width=-1080,
)
Spacing13 = VerticalArrangement(parent=Scope1, Height=-1002)
HistoryButton = Button(
    parent=Scope1,
    FontSize=24,
    Text='💾 Hi-story',
    BackgroundColor='&HFFFFC800',
    Width=-1080,
)
# endregion scope1

# region scope2
# Second "screen": Choose parameters for story
# Each input has a label and a random button above it, a horizontal scope, an input box
Scope2 = VerticalArrangement(Width=-1095, Height=-2, Visible=False, AlignHorizontal=3)
Buttons2 = HorizontalArrangement(parent=Scope2, Width=-2, AlignHorizontal=3)
CreateButton = Button(parent=Buttons2, Text='📝 Write story', Width=-2)
BackButton2 = Button(parent=Buttons2, Text='🏠', Width=-1015)
Spacing2 = VerticalArrangement(parent=Scope2, Height=50)
StyleScope = HorizontalArrangement(parent=Scope2, Width=-2, Height=75, AlignVertical=2)
StoryL1 = Label(
    parent=StyleScope,
    Text='This is a ...',
    Width=-2,
    TextAlignment=1,
    FontSize=24,
    FontBold=True,
)
StyleButton = Button(parent=StyleScope, Text='🔄', FontSize=24)
StyleInput = TextBox(
    parent=Scope2, Hint='fantasy, horror, ...', Width=-2, TextAlignment=1, FontSize=24
)
ThemeScope = HorizontalArrangement(parent=Scope2, Width=-2, Height=75, AlignVertical=2)
StoryL2 = Label(
    parent=ThemeScope,
    Text='... story about ...',
    Width=-2,
    TextAlignment=1,
    FontSize=24,
    FontBold=True,
)
ThemeButton = Button(parent=ThemeScope, Text='🔄', FontSize=24)
ThemeInput = TextBox(
    parent=Scope2, Hint='friendship, love, ...', Width=-2, TextAlignment=1, FontSize=24
)
CharScope = HorizontalArrangement(parent=Scope2, Width=-2, Height=75, AlignVertical=2)
StoryL3 = Label(
    parent=CharScope,
    Text='... with character ...',
    Width=-2,
    TextAlignment=1,
    FontSize=24,
    FontBold=True,
)
CharButton = Button(parent=CharScope, Text='🔄', FontSize=24)
CharInput = TextBox(
    parent=Scope2,
    Hint='Harry Potter, Cat in the Hat, ...',
    Width=-2,
    TextAlignment=1,
    FontSize=24,
)
Spacing22 = VerticalArrangement(parent=Scope2, Height=50)
CreateButton2 = Button(
    parent=Scope2,
    FontSize=24,
    Text='📝 Write story',
    BackgroundColor='&HFF66CC66',
    Width=-1080,
)
# endregion scope2

# region scope3
# Third "screen": The actual story
Scope3 = VerticalArrangement(Width=-1095, Height=-2, Visible=False)
Buttons3 = HorizontalArrangement(parent=Scope3, Width=-2)
ChPrevButton = Button(parent=Buttons3, Text='⬅', Width=-1015)
PlayButton = Button(parent=Buttons3, Text='⏯️', Width=-1015)
ChNextButton = Button(parent=Buttons3, Text='➡ Next chapter', Width=-2)
ShareButton = Button(parent=Buttons3, Text='🔗', Width=-1015)
BackButton3 = Button(parent=Buttons3, Text='🏠', Width=-1015)
Spacing3 = VerticalArrangement(parent=Scope3, Height=25)
StoryScroll = VerticalScrollArrangement(parent=Scope3, Height=-2)
StoryLabel = Label(parent=StoryScroll, Width=-2, FontSize=24)
# endregion scope3

# region scope4
# Fourth "screen": History
Scope4 = VerticalArrangement(Width=-1095, Height=-2, Visible=False, AlignHorizontal=3)
Buttons4 = HorizontalArrangement(parent=Scope4, Width=-2)
# Yes, I know. No, they are not reversed. They are exactly like they should be.
HistNextButton = Button(parent=Buttons4, Text='⬅', Width=-1015)
HistPrevButton = Button(parent=Buttons4, Text='➡', Width=-1015)
HistViewButton = Button(parent=Buttons4, Text='📖 Read', Width=-2)
HistDelButton = Button(parent=Buttons4, Text='🗑', Width=-1015)
BackButton4 = Button(parent=Buttons4, Text='🏠', Width=-1015)
HistPaginator = Label(
    parent=Scope4, Text='Loading...', FontSize=24, Width=-2, TextAlignment=1
)
Spacing4 = VerticalArrangement(parent=Scope4, Height=25)
HistoryL1 = Label(parent=Scope4, Text='This is a ...', FontSize=24, FontBold=True)
StyleHist = TextBox(
    parent=Scope4, Width=-2, TextAlignment=1, FontSize=24, Enabled=False
)
HistoryL2 = Label(parent=Scope4, Text='... story about ...', FontSize=24, FontBold=True)
ThemeHist = TextBox(
    parent=Scope4, Width=-2, TextAlignment=1, FontSize=24, Enabled=False
)
HistoryL3 = Label(
    parent=Scope4, Text='... with character ...', FontSize=24, FontBold=True
)
CharHist = TextBox(parent=Scope4, Width=-2, TextAlignment=1, FontSize=24, Enabled=False)
Spacing42 = VerticalArrangement(parent=Scope4, Height=25)
HistoryLabel = Label(parent=Scope4, Width=-2, TextAlignment=1, FontSize=24)
Spacing43 = VerticalArrangement(parent=Scope4, Height=50)
HistViewButton2 = Button(
    parent=Scope4,
    FontSize=24,
    Text='📖 Read story',
    BackgroundColor='&HFFFFC800',
    Width=-1080,
)
# endregion scope4

# endregion components

# region constants
STYLES = [
    'fantasy',
    'funny',
    'sad',
    'adventure',
    'fairy tale',
    'mystery',
    'romantic',
    'sci-fi',
    'magical',
    'futuristic',
]
THEMES = [
    'friendship',
    'love',
    'family',
    'prejudice',
    'coming of age',
    'survival',
    'freedom',
    'hope',
    'equality',
]
CHARACTERS = [
    'Winnie the Pooh',
    'The Very Hungry Caterpillar',
    'Paddington Bear',
    'Cat in the Hat',
    'The Little Prince',
    'Thomas the Tank Engine',
    'Geronimo Stilton',
    'Harry Potter',
]
STRINGS = {
    StyleButton: [StyleInput, STYLES],
    ThemeButton: [ThemeInput, THEMES],
    CharButton: [CharInput, CHARACTERS],
}
API_KEY = obfs_text(get_compile_env('CHATBOT_APIKEY'))
INDEX_VERSION = 4
INDEX_DEFAULT = '{"stories":[],"version":4}'
# endregion constants

cur_uuid = None
chapter = 1
story_index = {}
index_index = 0
story_sel = {}
from_history = False
chat_text = ''
is_playing = False


def settitle(title):
    Screen1.Title = title


def init():
    WriterBot.ApiKey = API_KEY
    Scope1.Visible = True
    Scope2.Visible = False
    Scope3.Visible = False
    Scope4.Visible = False
    settitle('Story Box')
    index_data = json.loads(TinyDB1.GetValue('index', INDEX_DEFAULT))
    if index_data['version'] != INDEX_VERSION:
        TinyDB1.ClearAll()
        index_data = json.loads(INDEX_DEFAULT)
    if index_data['stories']:
        last_uuid = index_data['stories'][-1]
        story = json.loads(TinyDB1.GetValue(str(last_uuid), 'null'))
        StyleInput.Text = story['style']
        ThemeInput.Text = story['theme']
        CharInput.Text = story['character']
    HistoryButton.Visible = bool(index_data['stories'])


def getuuid():
    return random.randrange(1, 1000000000)


def onstart():
    global cur_uuid, from_history
    Scope1.Visible = False
    Scope2.Visible = True
    Scope3.Visible = False
    Scope4.Visible = False
    StyleInput.Enabled = True
    ThemeInput.Enabled = True
    CharInput.Enabled = True
    CreateButton.Enabled = True
    BackButton2.Enabled = True
    CreateButton.Text = '📝 Write'
    settitle('New story')
    WriterBot.ResetConversation()
    cur_uuid = None
    from_history = False


def on_any_btn_click(btn, not_handled):
    if btn != PlayButton:
        TextToSpeech1.Speak('')
    if not_handled:
        if btn in STRINGS:
            comp: TextBox = STRINGS[btn][0]
            lst = STRINGS[btn][1]
            comp.Text = lst[random.randrange(len(lst))]


def showstory():
    StoryClock.TimerEnabled = False
    Scope1.Visible = False
    Scope2.Visible = False
    Scope3.Visible = True
    Scope4.Visible = False
    ChPrevButton.Enabled = chapter != 1
    PlayButton.Enabled = True
    ChNextButton.Enabled = not from_history or chapter < len(story_sel['chapters'])
    BackButton3.Enabled = True
    ShareButton.Enabled = True
    settitle('Chapter ' + str(chapter))
    StoryLabel.Text = story_sel['chapters'][chapter - 1]


def onresponse(response):
    global cur_uuid, chapter, story_sel
    if cur_uuid == None:
        cur_uuid = getuuid()
        index_str = TinyDB1.GetValue('index', INDEX_DEFAULT)
        index_data = json.loads(index_str)
        index_data['stories'].append(cur_uuid)
        TinyDB1.StoreValue('index', json.dumps(index_data))
        story_sel = {
            'style': StyleInput.Text,
            'theme': ThemeInput.Text,
            'character': CharInput.Text,
            'created_at': time.time(),
            'chapters': [response],
        }
    else:
        story_sel['chapters'].append(response)
    TinyDB1.StoreValue(str(cur_uuid), story_sel)
    showstory()


def converse(prompt):
    WriterBot.Converse(prompt)
    # onresponse('this is sample response. prompt: ' +prompt)


def onmodresponse(code, text):
    data = json.loads(text)
    if data['results'][0]['flagged']:
        Notifier1.ShowAlert("Your content violates OpenAI's content policies.")
        if Scope3.Visible:
            showstory()
        elif Scope2.Visible:
            onstart()
    else:
        converse(chat_text)


def checktext(text):
    global chat_text
    chat_text = text
    web_post(
        'https://api.openai.com/v1/moderations',
        callback=onmodresponse,
        data=json.dumps({'input': text}),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY,
        },
    )


def oncreate():
    global chapter, cur_uuid, story_sel
    if StyleInput.Text == 'clear.' and ThemeInput.Text == '' and CharInput.Text == '':
        TinyDB1.ClearAll()
        Notifier1.ShowAlert('Cleared all tags from DB')
        init()
        return
    if StyleInput.Text == '' or ThemeInput.Text == '' or CharInput.Text == '':
        Notifier1.ShowAlert(
            'Please fill in all the blanks, or click the button to randomize!'
        )
        return
    prompt = (
        "Write a children's story with the following parameters. Style: "
        + StyleInput.Text
        + '. Theme: '
        + ThemeInput.Text
        + '. Character: '
        + CharInput.Text
        + '.'
    )
    story_sel = {
        'style': StyleInput.Text,
        'theme': ThemeInput.Text,
        'character': CharInput.Text,
        'created_at': time.time(),
        'chapters': ['Loading, please wait...'],
    }
    chapter = 1
    showstory()
    ChPrevButton.Enabled = False
    PlayButton.Enabled = False
    ChNextButton.Enabled = False
    BackButton3.Enabled = False
    ShareButton.Enabled = False
    cur_uuid = None
    checktext(prompt)


def onchaterror(code, text):
    Notifier1.ShowAlert('Error creating story: ' + str(code) + ' ' + text)
    onstart()


def onprevchap():
    global chapter
    chapter -= 1
    showstory()


def onstoryplay():
    if is_playing:
        TextToSpeech1.Speak('')
    else:
        TextToSpeech1.Speak(story_sel['chapters'][chapter - 1])


def onstorystop():
    TextToSpeech1.Speak('')


def onnextchap():
    global chapter
    ChPrevButton.Enabled = False
    PlayButton.Enabled = False
    ChNextButton.Enabled = False
    BackButton3.Enabled = False
    ShareButton.Enabled = False
    chapter += 1
    if chapter <= len(story_sel['chapters']):
        showstory()
    else:
        story_sel['chapters'].append('Loading, please wait...')
        showstory()
        story_sel['chapters'].pop(len(story_sel['chapters']) - 1)
        ChPrevButton.Enabled = False
        PlayButton.Enabled = False
        ChNextButton.Enabled = False
        BackButton3.Enabled = False
        ShareButton.Enabled = False
        prompt = 'Continue the story.'
        converse(prompt)


def onsharestory():
    Sharing1.ShareMessage(story_sel['chapters'][chapter - 1])


def onhiststoryload(text):
    global story_sel
    story_sel = json.loads(text)
    style = story_sel['style']
    theme = story_sel['theme']
    character = story_sel['character']
    chapters = story_sel['chapters']
    StyleHist.Text = style
    ThemeHist.Text = theme
    CharHist.Text = character
    HistPaginator.Text = (
        'Story '
        + str(len(story_index['stories']) - index_index)
        + ' of '
        + str(len(story_index['stories']))
    )
    HistoryLabel.Text = (
        'Written at '
        + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(story_sel['created_at']))
        + '\n\nThere are '
        + str(len(chapters))
        + ' chapters.'
    )
    HistPrevButton.Enabled = index_index != 0
    HistViewButton.Enabled = True
    HistDelButton.Enabled = True
    HistNextButton.Enabled = index_index != len(story_index['stories']) - 1


def showhistory():
    story_uuid = story_index['stories'][index_index]
    HistPrevButton.Enabled = False
    HistViewButton.Enabled = False
    HistDelButton.Enabled = False
    HistNextButton.Enabled = False
    HistPaginator.Text = 'Loading...'
    onhiststoryload(TinyDB1.GetValue(str(story_uuid), 'null'))


def onhistoryload(text):
    global story_index, index_index
    story_index = json.loads(text)
    index_index = len(story_index['stories']) - 1
    if index_index < 0:
        HistPaginator.Text = 'No history stories.'
    else:
        showhistory()


def onhistory():
    global from_history
    Scope1.Visible = False
    Scope2.Visible = False
    Scope3.Visible = False
    Scope4.Visible = True
    HistPrevButton.Enabled = False
    HistViewButton.Enabled = False
    HistDelButton.Enabled = False
    HistNextButton.Enabled = False
    settitle('History')
    HistPaginator.Text = 'Loading...'
    from_history = True
    onhistoryload(TinyDB1.GetValue('index', INDEX_DEFAULT))


def onhistprev():
    global index_index
    index_index -= 1
    showhistory()


def onhistnext():
    global index_index
    index_index += 1
    showhistory()


def onhistview():
    global cur_uuid, chapter
    cur_uuid = story_index['stories'][index_index]
    chapter = 1
    showstory()
    StoryLabel.Text = ''
    StoryClock.TimerEnabled = True


def onhistdel():
    DeleteNotifier.ShowChooseDialog(
        'Are you sure you want to delete this story?',
        'Are you sure?',
        'Yes!',
        'No!',
        False,
    )


def onhistdelchs(choice):
    global story_index
    if choice == 'Yes!':
        story_index['stories'].pop(index_index)
        HistPrevButton.Enabled = False
        HistViewButton.Enabled = False
        HistDelButton.Enabled = False
        HistNextButton.Enabled = False
        TinyDB1.StoreValue('index', json.dumps(story_index))
        onhistoryload(json.dumps(story_index))


def onplaystart():
    global is_playing
    is_playing = True


def onplayend(success):
    global is_playing
    is_playing = False


def onback():
    global index_index
    if Scope3.Visible:
        if from_history:
            index = index_index
            onhistory()
            index_index = index
            showhistory()
        else:
            onstart()
    elif Scope2.Visible or Scope4.Visible:
        init()
    else:
        raise CloseApplication


def errhandler(comp, function, errno, message):
    if errno == 1103:  # network error
        Notifier1.ShowAlert(
            'Web request failed. Make sure you are connected to the Internet!'
        )
        onstart()
    else:
        Notifier1.ShowAlert(
            'Error ' + str(errno) + ' (at ' + str(function) + '): ' + message
        )
        init()


Screen1.on_Initialize(init)
StartButton.on_Click(onstart)
Button.on_any_Click(on_any_btn_click)
CreateButton.on_Click(oncreate)
CreateButton2.on_Click(oncreate)
WriterBot.on_GotResponse(onresponse)
WriterBot.on_ErrorOccurred(onchaterror)
ChPrevButton.on_Click(onprevchap)
PlayButton.on_Click(onstoryplay)
ChNextButton.on_Click(onnextchap)
ShareButton.on_Click(onsharestory)
HistoryButton.on_Click(onhistory)
HistPrevButton.on_Click(onhistprev)
HistNextButton.on_Click(onhistnext)
HistViewButton.on_Click(onhistview)
HistDelButton.on_Click(onhistdel)
HistViewButton2.on_Click(onhistview)
DeleteNotifier.on_AfterChoosing(onhistdelchs)

StoryClock.on_Timer(showstory)

TextToSpeech1.on_BeforeSpeaking(onplaystart)
TextToSpeech1.on_AfterSpeaking(onplayend)

BackButton2.on_Click(onback)
BackButton3.on_Click(onback)
BackButton4.on_Click(onback)
BackButton3.on_LongClick(init)
Screen1.on_BackPressed(onback)

Screen1.on_ErrorOccurred(errhandler)
