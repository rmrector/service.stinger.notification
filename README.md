# Stinger scene notification

This add-on notifies you of stinger scenes in the current movie. It pops up a notification when the credits roll (or at least towards the end). It uses tags to identify movies that have a stinger, which can be automatically added by the [Universal Movie Scraper](http://forum.kodi.tv/showthread.php?tid=129821) from [TheMovieDB](https://www.themoviedb.org/), as aftercreditsstinger and duringcreditsstinger.

If the video has chapters, it pops up when the last chapter starts, which is generally the credits, otherwise it pops up 10 (configurable) minutes before the movie ends.

There are also settings to add an additional tag to consider for both stinger types.

## Skinning

It works independently from skins, using a simple notification message by default. There is a skinnable window available if that's your style, with an example in resources/skins/Example/. The built in control labels are `id="100"` for the stinger type (During credits, After credits) and `id="101"` for the full message.

The window property **stinger** is set on the window **fullscreenvideo** when the video starts, for skins and such. Possible values for **stinger** are `duringcreditsstinger`, `aftercreditsstinger`, `duringcreditsstinger aftercreditsstinger` if the movie has both, and `None`. The property is only set when a movie in the library is playing, and empty in all other cases.
