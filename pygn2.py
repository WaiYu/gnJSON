"""
pygn.py

pygn (pronounced "pigeon") is a simple Python client for the Gracenote Music 
Web API, which can retrieve Artist, Album and Track metadata with the most 
common options.

You will need a Gracenote Client ID to use this module. Please contact 
developers@gracenote.com to get one.
"""

import xml.etree.ElementTree, urllib2, urllib, json
import xml.dom.minidom

# Set DEBUG to True if you want this module to print out the query and response XML
DEBUG = False

def register(clientID):
  """
  This function registers an application as a user of the Gracenote service
  
  It takes as a parameter a clientID string in the form of 
  "NNNNNNN-NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN" and returns a userID in a 
  similar format.
  
  As the quota of number of users (installed applications or devices) is 
  typically much lower than the number of queries, best practices are for a
  given installed application to call this only once, store the UserID in 
  persistent storage (e.g. filesystem), and then use these IDs for all 
  subsequent calls to the service.
  """
  
  # Create XML request
  query = _gnquery()
  query.addQuery('REGISTER')
  query.addQueryClient(clientID)
  
  queryXML = query.toString()
  
  # POST query
  response = urllib2.urlopen(_gnurl(clientID), queryXML)
  return xml.dom.minidom.parse(response)

def search(clientID='', userID='', artist='', album='', track='', toc=''):
  """
  Queries the Gracenote service for a track, album, artist, or TOC
  
  TOC is a string of offsets in the format '150 20512 30837 50912 64107 78357 ...' 
  """

  if clientID=='' or userID=='':
    print 'ClientID and UserID are required'
    return None

  if artist=='' and album=='' and track=='' and toc=='':
    print 'Must query with at least one field (artist, album, track, toc)'
    return None
  
  # Create XML request
  query = _gnquery()
  
  query.addAuth(clientID, userID)
  
  if (toc != ''):
    query.addQuery('ALBUM_TOC')
    query.addQueryMode('SINGLE_BEST_COVER')
    query.addQueryTOC(toc)
  else:
    query.addQuery('ALBUM_SEARCH')
    query.addQueryMode('SINGLE_BEST_COVER')
    query.addQueryTextField('ARTIST', artist)
    query.addQueryTextField('ALBUM_TITLE', album)
    query.addQueryTextField('TRACK_TITLE', track)
  query.addQueryOption('SELECT_EXTENDED', 'COVER,REVIEW,ARTIST_BIOGRAPHY,ARTIST_IMAGE,ARTIST_OET,MOOD,TEMPO')
  query.addQueryOption('SELECT_DETAIL', 'GENRE:3LEVEL,MOOD:2LEVEL,TEMPO:3LEVEL,ARTIST_ORIGIN:4LEVEL,ARTIST_ERA:2LEVEL,ARTIST_TYPE:2LEVEL')
  
  queryXML = query.toString()
  
  if DEBUG:
    print '------------'
    print 'QUERY XML'
    print '------------'
    print queryXML
  
  # POST query
  response = urllib2.urlopen(_gnurl(clientID), queryXML)
  
  if DEBUG:
    response2 = urllib2.urlopen(_gnurl(clientID), queryXML)
    responseXML = response2.read()
    print '------------'
    print 'RESPONSE XML'
    print '------------'
    print responseXML
  
  return xml.dom.minidom.parse(response)

class _gnquery:
  """
  A utility class for creating and configuring an XML query for POST'ing to
  the Gracenote service
  """

  def __init__(self):
    self.root = xml.etree.ElementTree.Element('QUERIES')
    
  def addAuth(self, clientID, userID):
    auth = xml.etree.ElementTree.SubElement(self.root, 'AUTH')
    client = xml.etree.ElementTree.SubElement(auth, 'CLIENT')
    user = xml.etree.ElementTree.SubElement(auth, 'USER')
  
    client.text = clientID
    user.text = userID
  
  def addQuery(self, cmd):
    query = xml.etree.ElementTree.SubElement(self.root, 'QUERY')
    query.attrib['CMD'] = cmd
  
  def addQueryMode(self, modeStr):
    query = self.root.find('QUERY')
    mode = xml.etree.ElementTree.SubElement(query, 'MODE')
    mode.text = modeStr

  def addQueryTextField(self, fieldName, value):
    query = self.root.find('QUERY')
    text = xml.etree.ElementTree.SubElement(query, 'TEXT')
    text.attrib['TYPE'] = fieldName
    text.text = value
  
  def addQueryOption(self, parameterName, value):
    query = self.root.find('QUERY')
    option = xml.etree.ElementTree.SubElement(query, 'OPTION')
    parameter = xml.etree.ElementTree.SubElement(option, 'PARAMETER')
    parameter.text = parameterName
    valueElem = xml.etree.ElementTree.SubElement(option, 'VALUE')
    valueElem.text = value
  
  def addQueryGNID(self, GNID):
    query = self.root.find('QUERY')
    GNIDElem = xml.etree.ElementTree.SubElement(query, 'GN_ID')
    GNIDElem.text = GNID
    
  def addQueryClient(self, clientID):
    query = self.root.find('QUERY')
    client = xml.etree.ElementTree.SubElement(query, 'CLIENT')
    client.text = clientID
    
  def addQueryRange(self, start, end):
    query = self.root.find('QUERY')
    queryRange = xml.etree.ElementTree.SubElement(query, 'RANGE')
    rangeStart = xml.etree.ElementTree.SubElement(queryRange, 'START')
    rangeStart.text = str(start)
    rangeEnd = xml.etree.ElementTree.SubElement(queryRange, 'END')
    rangeEnd.text = str(end)
  
  def addQueryTOC(self, toc):
    # TOC is a string of format '150 20512 30837 50912 64107 78357 ...' 
    query = self.root.find('QUERY')
    tocElem = xml.etree.ElementTree.SubElement(query, 'TOC')
    offsetElem = xml.etree.ElementTree.SubElement(tocElem, 'OFFSETS')
    offsetElem.text = toc
    
  def toString(self):
    return xml.etree.ElementTree.tostring(self.root)

  #Methods added by Fabian to reflect the Rhythm use case

  def addAttributeSeed(self, moodID, eraID, genreID):
    query = self.root.find('QUERY')
    seed = xml.etree.ElementTree.SubElement(query, 'SEED')
    seed.attrib['TYPE'] = "ATTRIBUTE"
    if genreID!='':
      genreElement = xml.etree.ElementTree.SubElement(seed, 'GENRE')
      genreElement.attrib['ID'] = genreID
    if moodID!='':    
      genreElement = xml.etree.ElementTree.SubElement(seed, 'MOOD')
      genreElement.attrib['ID'] = moodID
    if eraID!='':
      genreElement = xml.etree.ElementTree.SubElement(seed, 'ERA')
      genreElement.attrib['ID'] = eraID


  def addTextSeed(self, artist, track):
    query = self.root.find('QUERY')
    seed = xml.etree.ElementTree.SubElement(query, 'SEED')
    seed.attrib['TYPE'] = "TEXT"
    if artist!='':
      text = xml.etree.ElementTree.SubElement(seed, 'TEXT')
      text.attrib['TYPE'] = "ARTIST"
      text.text = artist
    if track!='':
      text = xml.etree.ElementTree.SubElement(seed, 'TEXT')
      text.attrib['TYPE'] = "TRACK"
      text.text = track
  
  def addQueryEVENT(self, eventType, gnID):
    query = self.root.find('QUERY')
    event = xml.etree.ElementTree.SubElement(query, 'EVENT')
    event.attrib['TYPE'] = eventType
    gnidTag = xml.etree.ElementTree.SubElement(event, 'GN_ID')
    gnidTag.text = gnID

  def addRadioID(self, radioID):
    query = self.root.find('QUERY')
    radio = xml.etree.ElementTree.SubElement(query, 'RADIO')
    myradioid = xml.etree.ElementTree.SubElement(radio, 'ID')
    myradioid.text = radioID