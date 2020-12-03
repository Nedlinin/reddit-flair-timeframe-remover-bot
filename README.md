# Reddit Flair Remover

This bot simply removes posts that have been flaired by AutoModerator if the post was created during the
specified day range (Monday-Wednesday for instance) and the flair matches the config.


## Installation
 1. Copy the config example to config.ini
 `cp config/config.ini.example config/config.ini`
 2. Create API account on [Reddit](https://www.reddit.com/dev/api/)
 3. Fill in the keys and passwords in the `config/config.ini` file
 4. Set the `SUBREDDIT` in `config/config.ini`
     - This only works when the Reddit account is moderator of the selected subreddit.
 5. Set `DAY_START` and `DAY_END` variables in `config/config.ini` file.
     - Python starts the week on Monday.  Keep this in mind as you add values.
     - To remove posts between Saturday and Sunday, use `DAY_START = Saturday` and `DAY_END = Sunday`
     - Note: We don't currently support multiple date ranges.
 6. Set `FLAIR_TO_REMOVE` to the flair class being used to determine removal needs.  If the flair class *contains* this value the post will be removed.
 7. Set `REMOVAL_REASON_ID` to the Reddit ID for the removal reason.
 8. Run using docker-compose:
    `docker-compose up -d`
