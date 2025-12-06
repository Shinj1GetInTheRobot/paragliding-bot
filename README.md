# paragliding-bot
Paragliding is fun, but checking the weather every day isn't. Let me do it for you!

Just a little script I wrote that checks the wind conditions at Bellambi on Willy Weather,
then sends me an email if any days look good.

Note, this is not intended for anyone else to use, sorry.

    - mail.py:      Authenticates and sends from the bot email (using the Google Gmail API)
                    Note: Gotta setup your own Gmail account for the bot.

    - config.json:  Stores the Willy Weather API key (get ur own!), 
                    the user's email account address,
                    the bot email account address.

    - main.py:      Checks if 24 hours has passed since the last check, if not aborts.
                    If yes, calls the bot, and writes a new entry in .log file.

    - bot.py:       Checks the wind conditions at Bellambi (using the WillyWeather API).