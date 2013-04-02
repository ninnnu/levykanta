import re
import urllib2, urllib, httplib
import sys
import simplejson
import MySQLdb

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from django.conf import settings

class NotFound(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Barcode():
	def __init__(self, barcode):
		self._barcode = barcode
		self._artist = None
		self._title = None
		self._tracks = []

	def __str__(self):
	  return str(self._artist+" - "+self._title)

	def get_artist(self):
		return self._artist

	def get_title(self):
		return self._title

	def get_tracks(self):
		return self._tracks

	def json(self):
		return simplejson.dumps({'artist': self._artist, 'title': self._title, 'tracks': self._tracks})

	def lookup_tracks(self, cd_id):
		print "Looking up tracks"
		if(len(self._tracks) > 0):
			return
		db = MySQLdb.connect(settings.DISCOGS_SERVER, settings.DISCOGS_USERNAME, settings.DISCOGS_PASSWORD, settings.DISCOGS_DATABASE)
		dbc = db.cursor()
		dbc.execute("""SELECT artist, title FROM discogs_tracks WHERE cd_id = %s""", (cd_id,))
		row = dbc.fetchone()
		while(row):
			self._tracks.append((row[0], row[1]))
			row = dbc.fetchone()
	
	def lookup(self):
		db = MySQLdb.connect(settings.DISCOGS_SERVER, settings.DISCOGS_USERNAME, settings.DISCOGS_PASSWORD, settings.DISCOGS_DATABASE)
		dbc = db.cursor()
		dbc.execute("SELECT id, artist, title FROM discogs WHERE barcode = %s", (self._barcode))
		row = dbc.fetchone()
		cd_id = row[0]
		self._artist = row[1]
		self._title = row[2]
		lookup_tracks(cd_id)
