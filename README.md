# Github Readme Kindle Syncer

# Automatic Kindle-Notion Syncer

# What does this app do?

Great question! 

**TLDR:** 

It automatically syncs all of the highlights and notes that you make on the kindle app right to a Notion database at any interval of your choosing! It’s completely free, set it up once and never worry about your notes being out of sync again!

**More Background:**

There are other apps that do this (namely Readwise), but they all charge a monthly subscription charge for this service. For those of us that don’t have this extra money lying around or don’t want to pay monthly for a service that we can code up in a few hours, this seems ridiculous. For anyone checking out this github page, this choice is even easier for you to make since you don’t have to code anything yourself! I’ve already put this together for you, and in about 10 minutes, you can set this service up and save yourself that monthly fee.

**Go from this:**

![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled.png)

**To this: (Automatically!)**

![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%201.png)

Awesome right?!

# Installation Instructions

<aside>
⚡ Please note, these instructions look long, but only because I walk you through it step-by-step and added lots of pictures. Please let me know if I can make anything more clear.

</aside>

1. Set up Notion
    1. Duplicate this template to your notion account: [https://www.notion.so/bfc244c3ef04467cb774cdb27ed4e4b6?v=f0563ad6f47f480aa9d643a2f6c17e44](https://www.notion.so/bfc244c3ef04467cb774cdb27ed4e4b6)
        1. Note: feel free to add properties to this database, but the “Title” and “Author” properties shouldn’t be renamed.
    2. Save the database id somewhere
        1. Copy the url for your database. It should look like this: [https://www.notion.so/lucas-gen/e32a031992f348aeae115fe6dee83583?v=1e75f5e2b07349f4b331e88c4ca3beac](https://www.notion.so/e32a031992f348aeae115fe6dee83583)
        2. The database id is this sequence of letters and numbers
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%202.png)
            
        3. Copy and save this somewhere
    3. Create an integration
        1. Go to [https://www.notion.com/my-integrations](https://www.notion.com/my-integrations).
        2. Click the "+ New integration" button.
        3. Give your integration a name - e.g. "Kindle Syncer".
        4. Select the workspace where you want to install this integration.
        5. Select the capabilities that your integration will have (select them all).
        6. Click "Submit" to create the integration.
        7. Copy the "Internal Integration Token" on the next page and save it somewhere secure, e.g. a password manager.
        8. Here’s my settings for reference:
            - Image Here
                
                ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%203.png)
                
2. Now that we have that information, let’s set up the Kindle Syncer
    1. Make sure you have git installed: see [here](https://github.com/git-guides/install-git) (it’s probably already installed but come back to this if you find out it’s not)
    2. Create a free heroku account if you don’t have one. [Link Here](https://signup.heroku.com/)
    3. Install the Heroku CLI [here](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli):
    4. Open your terminal and link Heroku CLI to your heroku account. (copy and paste the below code into terminal)
        
        ```bash
        heroku login
        ```
        
    5. Clone Repository, locally and then make a heroku app from it
        
        ```bash
        git clone https://github.com/lg08/kindle_notion_syncer.git
        cd kindle_notion_syncer
        heroku create -a kindle-notion-syncer
        git push heroku master
        
        ```
        
    6. Now go to [https://dashboard.heroku.com/apps](https://dashboard.heroku.com/apps) and click on the app called “kindle-notion-syncer”, and then click on settings.
        - Images Here
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%204.png)
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%205.png)
            
    7. Scroll Down to Buildpacks and add the following buildpacks:
        1. heroku/python
        2. https://github.com/heroku/heroku-buildpack-google-chrome
        3. https://github.com/heroku/heroku-buildpack-chromedriver
        - Image Here
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%206.png)
            
    8. Now add the Config Variables
        1. CHROMEDRIVER_PATH = /app/.chromedriver/bin/chromedriver
        2. GOOGLE_CHROME_BIN = /app/.apt/usr/bin/google-chrome
        3. AMAZON_EMAIL=your_email
        4. AMAZON_PASSWORD=your_password
        5. database_ID=your_database_id_that_we_saved_earlier
        6. secret_Key=your_secret_key_that_we_saved_earlier
            1. aka, the "Internal Integration Token" that we saved earlier
        - Image Here
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%207.png)
            
    9. Now click on the “Resources” tab in heroku, search for an add-on called “Heroku Scheduler”
    10. Hit Submit Order Form (Don’t worry it’s free)
        - Image Here
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%208.png)
            
    11. Now click on “Heroku Scheduler” and it will take you to a new tab
        
        ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%209.png)
        
    12. Hit “Create Job”
        - Image Here
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%2010.png)
            
    13. Now set up how often you want your notes to sync.
        1. Under “Schedule” choose how often you want your notes to sync - I set them to sync only once a day since I don’t really need them to sync any more frequently than this
        2. Under “Run Command” enter `python3 kindle_notion_syncer.py`
        3. Hit “Save Job”
        - Image Here
            
            ![Untitled](Github%20Readme%20Kindle%20Syncer%200779a6c4c7d843eea2e6e938ddffeb2d/Untitled%2011.png)
            
3. That’s it!! Congrats, you’re done! Now just sit back, read your books, and know that they will be automatically synced to your Notion database