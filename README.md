# Discord Friend
This is a simple bot for discord that I created. It runs asynchronously in a seperate python terminal that you can run. There are commands you can type in discord for it, and it will run them and display the result in your discord server.

## How to add to a discord server
1. First make sure you are logged into discord and have a server to add the bot
2. Go into the developer portal, OAuth2, select bot and go to the link provided. Bot set to private so it isn't added to servers by random people.

## How to run this bot
First of all you need to make sure the bot is added to your discord server. Make sure to refer to the note above. Once it is added, simply run *python main.py* in a command prompt to begin the bot. It will send a message in the terminal once it is logged on. Planning on running this bot on a raspberry pi at some point so it is always online and all you need to do is add it to a server. In the meantime it must be run locally.
Make sure that the bot's token is saved in a .txt file called *token.txt* in the same folder as *main.py*. The bot reads this text file for the token.

For any commands requiring Reddit's API, you need to save it in a file titled *praw.txt* in the same directory as *main.py*. In it, you should have 3 things formatted as such:
- Client ID in the first line
- Client secret in the second line
- Client Agent in the 3rd line

I don't have these files in the repo for security sake.