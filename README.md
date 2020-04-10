# Agent-IPA-2020-03-21-GRP-Etika

## SECTION 1 : AIRBNB Agent
## NUS ISS Intelligent Agent
<img src="Images/chatbot.png"
     style="float: left; margin-right: 0px;" />

<br>
---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT

To be completed

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| LIM LI WEI | A0087855L | --- | E0319479@u.nus.edu |
| PREM CHANDRAN | A--- | --- | --- |
| YONG QUAN ZHI, TOMMY | A0195353Y | ---| E0384984@u.nus.edu |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[NUS ISS AIRBNB AGENT](https://youtube.com)


---

## SECTION 5 : USER GUIDE

`<Download the user guide>` : <https://github.com/>

Download the guide from the link above for a more detailed description on how to configure, install, deploy the necessary components for this project. 

Please ensure you are using python 3.6 or higher.
Once you have downloaded and unzipped the project file, CD into your project root folder "<your-file-path>/ISA-IPA-2020-03-21-IS01PT-GRP-Etika-AirbnbAgent"

**Step 1**. Create a python env.
"python3 -m venv env" OR use "python -m venv env"

**Step 2**. Activate the python env. You should see (env) next to your command line.
For Mac: "source env/bin/activate"
For Windows: "env\Scripts\activate"

**Step 3**. Enter "pip install -r requirements.txt" OR "pip3 install -r requirements.txt". This will install all the required dependencies.

**Step 4**. Once installation is complete, enter " flask run". This will deploy your server locally on your pc.

**Step 5**. You need to open a channel to your computer so that dialogflow and the telegram bot can communicate with your server. To do this, we will use ngrok. With a new command prompt/terminal CD to the project root folder "<your-file-path>/ISA-IPA-2020-03-21-IS01PT-GRP-Etika-AirbnbAgent". There will be an "ngrok_win" and an "ngrok_mac" file. Rename the file with your OS in use to just "ngrok". E.g If you are using Windows, delete the "_win" from "ngrok_win".
From your command prompt, enter "ngrok http localhost:5000".
Take note of the https link. It should look something like this "https://f34bb6f6.ngrok.io". Take note of this link.

**Step 6**. Go to https://dialogflow.cloud.google.com/ and log in with your account. Proceed to iImport the dialogflow agent(IPA-AIRBNB.zip) on dialogflow.
To do this, first create a new agent and give it a name e.g. "AIRBNB AGENT".
Once created click on the settings gear icon next the agent name and click the "Export and Import" tab.
Click "Import From Zip" and select the IPA-AGENT zip file. Type in "IMPORT" into the text box and click "IMPORT".

**Step 7**. Once the agent has been imported and training is done, click on the "Fulfillment" option on the left menu bar. Enable the webhook(If it is not enabled), and copy and paste the ngrok https link on the URL field. Add in "/get_recommendations" right at the end of the ngrok link. Scroll to the bottom and click save. Give it some time to save your settings.

**Step 8**. Now open up your telegram app. From the search bar of your chat page, type "IPAAIRBNBBot" click on the result. A chat window will be created with the bot, click 'Start'. You can now test sending some search queries such as "Can you find some recommendations for 2 adults, 1 child and 1 infant to stay in Vienna from 5th June to 17th June?".

**Additional notes**: You can also test dialogs from the google assistant via the dialogflow website located on the right side of the screen.
Try to paste the following dialog in the chat field.

---

## SECTION 6 : PROJECT REPORT / PAPER

`<Download the Project Report>` : <https://github.com/>

## SECTION 7 : MISCELLANEOUS

### App URL: [NUS ISS AIRBNB AGENT]()
- the Chatbot system hosted on ...
