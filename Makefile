StoryBox.aia: main.py
	python3 -m py2ai create 'Story Box' StoryBox.aia --screen main.py Screen1 --asset magic-box.png --asset icon.png

.ai_session: token.txt
	python3 -m py2ai.appinventor auth `cat token.txt`

all: StoryBox.aia

auth: .ai_session

upload: auth StoryBox.aia
	python3 -m py2ai.appinventor upload StoryBox.aia --autoload
