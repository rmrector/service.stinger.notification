# Stinger scene notification

This add-on notifies you of stinger scenes in the current movie. It pops up a notification when the credits roll (or at least towards the end). It uses tags to identify movies that have a stinger, which can be automatically added by the [Universal Movie Scraper](http://forum.kodi.tv/showthread.php?tid=129821) from [The Movie Database](https://www.themoviedb.org/), as aftercreditsstinger and duringcreditsstinger.

If there are no chapters on your media file, the add-on searches for them on the [ChapterDb](http://www.chapterdb.org/). If chapters are available, the notification pops up when the last chapter starts, which is generally the credits, otherwise 10 (configurable) minutes before the movie ends.


### Adding tags

To add these tags to new movies automatically, set the Universal Movie Scraper as your movie scraper, and configure it to 'Get Keywords and Save as Tags from' themoviedb.org.

If your existing movies don't already have these tags, you can avoid rescraping them with a handy once-off option in the add-on settings under "Advanced", "Grab stinger tags from TheMovieDB for all movies", which will run through your library and grab these tags for all movies from The Movie Database. New movies should still be tagged by the scraper as described above.

### Skinning

It has a simple skinnable window, and offers viewers the option to use a simple notification message. The built in control labels are `id="100"` for the stinger type (During credits, After credits) and `id="101"` for the full message.

The window property **stinger** is set on the window **fullscreenvideo** when the video starts, for skins and such. Possible values for **stinger** are `duringcreditsstinger`, `aftercreditsstinger`, `duringcreditsstinger aftercreditsstinger` if the movie has both, and `None`. The property is only set when a movie in the library is playing, and empty in all other cases.

### Gotchas

Movies don't always start the last chapter when the credits begin rolling, so the notification won't be timed right for a handful of movies.
