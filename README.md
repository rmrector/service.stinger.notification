# Stinger scene notification

This add-on notifies you of stinger scenes in the current movie. It pops up a notification when the credits roll (or at least towards the end). It uses tags to identify movies that have a stinger, which can be automatically added by the [Universal Movie Scraper](http://forum.kodi.tv/showthread.php?tid=129821) from [The Movie Database](https://www.themoviedb.org/), as aftercreditsstinger and duringcreditsstinger.

If the video has chapters, it pops up when the last chapter starts, which is generally the credits, otherwise it pops up 10 (configurable) minutes before the movie ends.

### Adding tags

To add these tags to new movies automatically, set the Universal Movie Scraper as your movie scraper, and configure it to 'Get Keywords and Save as Tags from' themoviedb.org.

If your existing movies don't already have these tags, you can avoid rescraping them with a handy once-off option in the add-on settings, "Grab stinger tags for all movies", which will run through your library and grab these tags for all movies from The Movie Database. New movies should still be tagged by the scraper as described above.

There are also settings to add an additional tag to consider for both stinger types.

### Skinning

It has a simple skinnable window, and offers viewers the option to use a simple notification message. The built in control labels are `id="100"` for the stinger type (During credits, After credits) and `id="101"` for the full message.

The window property **stinger** is set on the window **fullscreenvideo** when the video starts, for skins and such. Possible values for **stinger** are `duringcreditsstinger`, `aftercreditsstinger`, `duringcreditsstinger aftercreditsstinger` if the movie has both, and `None`. The property is only set when a movie in the library is playing, and empty in all other cases.

### Gotchas

1. If your video doesn't have chapters, the notification pops up X minutes before the movie ends, which often enough will be while the movie is still ending, or after the credits have started, no matter the value of X.  
2. A chunk of movies don't have a separate chapter for the credits, so the notification pops up before the credits. Examples are Dogma and Ferris Bueller's Day Off.

### What's next?

Maybe grab missing chapters from the [ChapterDb](http://www.chapterdb.org/) API, slaying gotcha #1.
