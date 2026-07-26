# Ceremony-bot
It massively speeds up the medal logging process by automatically reading from a downloaded plain text version of ceremony documents. It fills out the name of each person, regiment, roblox profile link, medal and clasp. The Korps, Reason, Date and person who logged the medals will still be inputed manually but it can be easily copy-pasted. It works by outputing an excel file which you can finish completing, then copying over the logged medals to the actual sheet by pressing CTRL+C to copy then CTRL+SHIFT+V. DO NOT CTRL+V as it will paste it unformatted and it will look horrendous.

# Requirements

- Windows 10/11
- Python 3.12 or newer

Download Python here:

https://www.python.org/downloads/

# How to install (Windows)
Open command prompt, then navigate to the folder where you want to copy the program. For example:
```cmd
cd Desktop
```
Then to actually pull the files from the github, you do:
```cmd
git clone https://github.com/Cosmin127/Ceremony-bot.git
```
Go inside the folder of the application:
```cmd
cd Ceremony-bot
```
Make the python environment for the python scripts to run:
```cmd
python -m venv .venv
.venv\bin\activate
pip install -r requirements.txt
```

# How to use and run
First, make sure the algorithm knows what medals you're going to log, so edit config.py. There will be more instructions inside.

Download the ceremony document in plain text, then rename it to ceremony.txt and put it in the root of the application, aka next to the python scripts. Then run:
```cmd
cd Desktop\Ceremony-bot
.venv\bin\activate
python main.py ceremony.txt
```
The Excel file will be inside the output folder.
