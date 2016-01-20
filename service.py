import json
import os
import sys
import xbmc
import xbmcaddon

addon = xbmcaddon.Addon()
resourcelibs = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
resourcelibs = os.path.join(resourcelibs, u'resources', u'lib')
sys.path.append(resourcelibs)

from notificationwindow import NotificationWindow

DURING_CREDITS_STINGER_MESSAGE = 32000
AFTER_CREDITS_STINGER_MESSAGE = 32001
BOTH_STINGERS_MESSAGE = 32002
DURING_CREDITS_STINGER_TYPE = 32003
AFTER_CREDITS_STINGER_TYPE = 32004
DURING_CREDITS_STINGER_TAG = 'duringcreditsstinger'
AFTER_CREDITS_STINGER_TAG = 'aftercreditsstinger'
BOTH_STINGERS_PROPERTY = DURING_CREDITS_STINGER_TAG + ' ' + AFTER_CREDITS_STINGER_TAG

def log(message, level=xbmc.LOGDEBUG):
    xbmc.log('[%s] %s' % (addon.getAddonInfo('id'), message), level)

class StingerService(xbmc.Monitor):
    def __init__(self):
        super(StingerService, self).__init__()
        self.reset()
        self.get_settings()

    def reset(self):
        self.currentid = None
        self.totalchapters = None
        self._stingertype = None
        xbmc.executebuiltin('ClearProperty(stinger, fullscreenvideo)')
        self.notified = False

    def get_settings(self):
        self.aftercredits_tag = addon.getSetting('aftercreditsstinger_tag')
        self.duringcredits_tag = addon.getSetting('duringcreditsstinger_tag')
        try:
            self.whereis_theend = int(addon.getSetting('timeremaining_notification'))
        except ValueError:
            self.whereis_theend = 10

    @property
    def stingertype(self):
        return self._stingertype

    @stingertype.setter
    def stingertype(self, value):
        self._stingertype = value
        xbmc.executebuiltin('SetProperty(stinger, %s, fullscreenvideo)' % value)

    def run(self):
        log('Started', xbmc.LOGINFO)
        while not self.waitForAbort(5):
            if self.currentid:
                self.check_for_display()
        log('Stopped', xbmc.LOGINFO)

    def onNotification(self, sender, method, data):
        if method not in ('Player.OnPlay', 'Player.OnStop'):
            return
        data = json.loads(data)
        if not data or 'item' not in data or 'id' not in data['item'] or data['item'].get('type') != 'movie':
            return
        if method == 'Player.OnStop':
            self.reset()
            return
        if self.currentid:
            return # Player.OnPlay is resuming from pause, and the rest needn't run again
        self.currentid = data['item']['id']

        movie = get_movie_details(self.currentid, ['tag'])
        if not movie or 'tag' not in movie or not movie['tag']:
            self.stingertype = None
        else:
            duringcredits = DURING_CREDITS_STINGER_TAG in movie['tag'] or self.duringcredits_tag and self.duringcredits_tag in movie['tag']
            aftercredits = AFTER_CREDITS_STINGER_TAG in movie['tag'] or self.aftercredits_tag and self.aftercredits_tag in movie['tag']
            if duringcredits and aftercredits:
                self.stingertype = BOTH_STINGERS_PROPERTY
            elif duringcredits:
                self.stingertype = DURING_CREDITS_STINGER_TAG
            elif aftercredits:
                self.stingertype = AFTER_CREDITS_STINGER_TAG
            else:
                self.stingertype = None

        if self.stingertype:
            try:
                self.totalchapters = int(xbmc.getInfoLabel('Player.ChapterCount'))
            except ValueError:
                self.totalchapters = None

    def check_for_display(self):
        if self.totalchapters:
            if self.on_lastchapter():
                self.notify()
        else:
            if self.near_endofmovie():
                self.notify()

    def on_lastchapter(self):
        try:
            return int(xbmc.getInfoLabel('Player.Chapter')) == self.totalchapters
        except ValueError:
            return False

    def near_endofmovie(self):
        try:
            timeremaining = int(xbmc.getInfoLabel('Player.TimeRemaining(hh)')) * 60 + int(xbmc.getInfoLabel('Player.TimeRemaining(mm)'))
            return timeremaining < self.whereis_theend
        except ValueError, ex:
            log('Having trouble where no trouble should be had, "%s".' % ex, xbmc.LOGWARNING)
            return False

    def notify(self):
        if self.notified:
            return
        self.notified = True
        message = None
        if self.stingertype == DURING_CREDITS_STINGER_TAG:
            message = addon.getLocalizedString(DURING_CREDITS_STINGER_MESSAGE)
            stingertype = addon.getLocalizedString(DURING_CREDITS_STINGER_TYPE)
        elif self.stingertype == AFTER_CREDITS_STINGER_TAG:
            message = addon.getLocalizedString(AFTER_CREDITS_STINGER_MESSAGE)
            stingertype = addon.getLocalizedString(AFTER_CREDITS_STINGER_TYPE)
        elif self.stingertype == BOTH_STINGERS_PROPERTY:
            message = addon.getLocalizedString(BOTH_STINGERS_MESSAGE)
            stingertype = '{0}, [LOWERCASE]{1}[/LOWERCASE]'.format(addon.getLocalizedString(DURING_CREDITS_STINGER_TYPE), addon.getLocalizedString(AFTER_CREDITS_STINGER_TYPE))
        if not message:
            return
        try:
            window = NotificationWindow('script-stinger-notification-Notification.xml', addon.getAddonInfo('path'), 'Default', '1080i')
            window.message = message
            window.stingertype = stingertype
            window.show()
            self.waitForAbort(6.5)
            window.close()
        except RuntimeError:
            # Use a simple notification if it is not skinned
            xbmc.executebuiltin('Notification("{0}", "{1}", 6500, special://home/addons/service.stinger.notification/resources/media/logo.png)'.format(stingertype, message))

    def onSettingsChanged(self):
        self.get_settings()

def get_movie_details(movie_id, properties=None):
    json_request = {'jsonrpc': '2.0', 'method': 'VideoLibrary.GetMovieDetails', 'params': {}, 'id': 1}
    json_request['params']['movieid'] = movie_id
    if properties:
        json_request['params']['properties'] = properties

    json_result = json.loads(xbmc.executeJSONRPC(json.dumps(json_request)))

    if 'result' in json_result and 'moviedetails' in json_result['result']:
        return json_result['result']['moviedetails']

if __name__ == '__main__':
    service = StingerService()
    try:
        service.run()
    finally:
        del service
