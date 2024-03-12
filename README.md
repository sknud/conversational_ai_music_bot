# conversational_ai_music_bot

![cover_photo.jpg](_09dec6e1-4851-4744-974c-d6fe37895f71.jpg)
_09dec6e1-4851-4744-974c-d6fe37895f71.jpg

This repo is a work in progress. It demonstrates a music chatbot that can converse with users about music use cases.

The following functionality is currently coverered:

###### For recommendations:
- music recommendations via artist
- music recommendations via song title

###### For music trivia questions:
- Album Release Date Questions
- Album Tracklist Questions
- Artist Biography Questions

## Pre-requisites
Check if your Python env is already configured
python3 --version
pip3 --version

Mac Instructions. For Windows or Linux, please see here: https://rasa.com/docs/rasa/installation/environment-set-up
1. Install homebrew if you haven't already (https://brew.sh/)
2. Update homebrew: brew update
3. brew install python

## Clone the repo
1. See https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository for more details.

## How to set up your RASA environment, using Python version 3.9
How to set up
1. Create a virtual env using python 3.9: python3.9 -m venv ./venv
2. Activate the virtual env: source ./venv/bin/activate
3. Make sure pip is up to date: pip3 install -U pip
4. Install rasa: pip3 install rasa
5. Install other requirements: pip install -r requirements.txt
6. Next you need to set up your client credentials, see the next section

## How to set up client credentials. For example, for use of the Spotify API
1. Go to the .env.example file in the root directory
2. Rename .env.example to .env
3. Add the credentials in for each. The services needed are listed below:
    - Spotify: https://developer.spotify.com/documentation/web-api
    - Last FM: https://www.last.fm/api/authentication


## Run rasa train to train the model

## Install Streamlit
1. pip install streamlit
2. Check it is working (streamlit will launch in a browser window): streamlit hello
3. To stop the Streamlit server, press: ctrl-C
4. Press deactivate if you want to exist the venv

## How to run and test the bot manually
1. Run the rasa server: rasa run -m models --enable-api --cors="*" or rasa run -m models --enable-api --cors="*" --debug
    * we use --cors"*" (Cross Origin Resource Sharing) to allow all traffic to connect. In production we set cors to only accept requests from specific origins
2. Split terminal
3. Run the action server rasa run actions (make sure you are in the correct folder!)
4. Split terminal again
5. In the new split terminal, run the streamlit app (make sure you are in the correct folder, cd streamlit): streamlit run main.py
6. The app will launch in a new window!

7. Alternatively; just run this to test the bot in the command line: rasa shell nlu

## How to train the model
1. Make changes
2. Run: rasa train
3. Use above steps

### How to run tests ###

## Unit Tests ##

## 1. How to test each function using pytest
1. Run: pytest

## Model Testing - Natural Language Understanding (NLU) ##

## 1. Testing each story using rasa test
1. Run: rasa test --stories tests/test_stories.yml


## 2. Cross Validating the model
This will perform NLU model evaluation with cross-validation by splitting the training data into multiple sets and training/testing the model several times to get an average performance metric
1. run: rasa test nlu --cross-validation

## 3. Test the the entire project (NLU, stories/rules, end-to-end conversations)
This will test:
- NLU evaluation: how well the model classifies intents and extracts entities based on the provided examples in the NLU training data using metrics such as precision, recall, and f1-score for intents and entities
- Dialogue Management (Core): tests stories and rules
- [Not utilising] End to End testing: test conversations if end-to-end examples are place in the tests/ directory
1. run: rasa test

