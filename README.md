# Agent-IPA-2020-03-21-GRP-Etika

## SECTION 1 : AIRBNB Agent
## NUS ISS Intelligent Agent
<img src="Miscellaneous/picture1.png"
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

`<Github File Link>` : <https://github.com/>

Download the guide from the link above and follow the instructions to deploy the chatbot locally.
Please ensure you are using python 3.6 or higher.
Once you have downloaded and unzipped the project file, CD into your project root folder "./ISA-IPA-2020-03-21-IS01PT-GRP-Etika-AirbnbAgent"

1. Create a python env <br>
python3 -m venv env

OR

python -m venv env

2. Activate the python env. You should see (env) next to your command line <br>
source env/bin/activate

OR Windows

env/Scripts/activate

3. Enter "pip install -r requirements.txt". This will install the required dependencies.

4. Once installation is complete, enter " flask run".

5. Launch ngrok. With a new command prompt/terminal CD to the project root folder. "./ISA-IPA-2020-03-21-IS01PT-GRP-Etika-AirbnbAgent" <br>
Enter "ngrok http localhost:5000" <br>
Take note of the https link. It should look something like this "https://f34bb6f6.ngrok.io"

6. Import the dialogflow agent on dialogflow. Go to https://dialogflow.cloud.google.com/ and log in with your account. <br>
Create a new agent and give it a name e.g. "AIRBNB AGENT". <br>
Once create click on the settings gear icon next the agent name and click the "Export and Import" tab. <br>
Click "Import From Zip" and select the IPA-AGENT zip file. Type in "IMPORT" into the text box and click "IMPORT".

7. Once the agent has been imported and training is done, click on the "Fulfillment" option on the left menu bar. Enable the webhook(If it is not enabled), and
copy and paste the ngrok https link on the URL field. Add in "/get_recommendations" right at the end of the ngrok link. Scroll to the bottom and click save.

8. Now you are ready to test dialogs from the google assistant from the right side of the screen. <br>
Try to paste the following dialog in the chat field. <br>
"Can you find some recommendations for 2 adults, 1 child and 1 infant to stay in Vienna from 5th June to 17th June?"

---

## SECTION 6 : PROJECT REPORT / PAPER

`<Github File Link>` : <https://github.com/>

## SECTION 7 : MISCELLANEOUS

### App URL: [NUS ISS AIRBNB AGENT]()
- the Chatbot system hosted on ...
