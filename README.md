# mtgled
MTG table LED project

![Configuration Screenshot](https://i.imgur.com/AYlI8HB.png)

This will be used to control LEDs installed on a card table for Magic: the Gathering multiplayer games.

It consists of a SPA frontend for:
- configuring game settings such as player names, locations, and color preferences
- showing the status of all LEDs on the table
- controlling game flow (start game, end game, eliminate player, pass turn, etc)

And a python backend for:
- controlling LEDs
- holding game state
