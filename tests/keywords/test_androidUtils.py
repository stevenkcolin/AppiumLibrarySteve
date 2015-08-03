import logging
import sys
import unittest
import appium
import mock

from AppiumLibrary.keywords import _ApplicationManagementKeywords
from webdriverremotemock import WebdriverRemoteMock
from AppiumLibrary.keywords import _AndroidUtilsKeywords


logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(stream_handler)
   
class AndroidUtilsTests(unittest.TestCase):
    am=None
    au=None

    def tearDown(self):
        self.am.close_all_applications()

    def setUp(self):
        self.am = _ApplicationManagementKeywords()
        self.am._debug = mock.Mock()
        # Uncomment to use Mock / Comment to test against real appium instance
        appium.webdriver.Remote = WebdriverRemoteMock
        # log debug from _ApplicationManagementKeywords to console
        self.am._debug = logger.debug
        self.am.open_application('http://10.1.160.124:4724/wd/hub', alias='MsB1', deviceName='MsB1', udid='d81e91ba', platformVersion='4.4', appPackage='com.android.contacts', platformName='Android', appActivity='.activities.DialtactsActivity')    
        self.au = _AndroidUtilsKeywords()
        self.au._current_application = self.am._current_application

    def test_set_network_connection_status(self):
        self.au.set_network_connection_status(4)

    def test_get_network_connection_status(self):
        self.au.get_network_connection_status()

    def test_push_pull_file(self):
        myFile='VGhpcyBpcyBteUZpbGUgYXMgYmFzZTY0' #'This is myFile as base64'
        #logger.debug('Pushing myFile as base64: %s' % (myFile, ))
        self.au.push_file('/storage/sdcard0/foo.txt', myFile)
        myFile=self.au.pull_file('/storage/sdcard0/foo.txt')
        #logger.debug('Pulled myFile as base64: %s' % (myFile, ))
        self.assertRegexpMatches(myFile, 'VGhpcyBpcyBteUZpbGUgYXMgYmFzZTY0')
        myFile=self.au.pull_file('/storage/sdcard0/foo.txt', decode=True)
        #logger.debug('Pulled myFile as Text: %s' % (myFile, ))
        self.assertRegexpMatches(myFile, 'as base64')
        myFile='This is myFile as Text'
        #logger.debug('Pushing myFile as Text: %s' % (myFile, ))
        myFile=self.au.push_file('/storage/sdcard0/foo.txt', myFile, encode=True)
        myFile=self.au.pull_file('/storage/sdcard0/foo.txt')
        #logger.debug('Pulled myFile as base64: %s' % (myFile, ))
        self.assertRegexpMatches(myFile, 'VGhpcyBpcyBteUZpbGUgYXMgVGV4dA==')
        myFile=self.au.pull_file('/storage/sdcard0/foo.txt', decode=True)
        #logger.debug('Pulled myFile as Text: %s' % (myFile, ))
        self.assertRegexpMatches(myFile, 'as Text')
