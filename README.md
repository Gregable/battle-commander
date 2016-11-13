Battle Commander
================

![Battle Commander screenshot](http://i.imgur.com/c0A321y.png)

This is a simple webapp that shows two different views of a tabletop
game (such as D&D) encounter in two different browser windows.

The first view (`/commander`) shows detailed information about all of
the combatants that the game master is managing. The second view
(`/viewer`) shows the same data with some information hidden such as
exact hitpoints of the minions or hidden notes.

This is intended to be used when projecting one browser tab to a different
screen with say a [ChromeCast](http://www.google.com/chrome/devices/chromecast/)
since the commander tab can then control the projected one. This isn't
intended to be exposed to the internet.

Python required.

How to run the server:

```shell
python commander.py
```

Then go to <http://localhost:8081/commander> for the admin page and to
<http://localhost:8081/viewer> for the viewer page.

`commander.py` has a few static variables at the top which you may want to
tweak.


Developing
----------

Feel free to make suggestions or pull requests. I don't want to add too many
bells and whistles though, I'd rather keep it simple. Most of the fields are
free-form text, so it's easy enough for the user to use them for anything.

The basic structure of the webapp is that there is an HTML div on
commander.html which is mirrored over to viewer.html twice a second via XHR
requests. That's all server.py does.

The actual logic for manipulating the page is in javascript in commander.html.
This includes stuff such as selecting the healthy/poor/dead conditions, rotating
through color markers, initiative rolls, etc.

Differences in what is displayed between the two pages are controlled via
different CSS rules in the two pages. The content in the shared div is always
identical.
