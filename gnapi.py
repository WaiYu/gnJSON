from flask import Flask
from flask import request, render_template
import json
from pygn2 import register, search, getNodeContent
app = Flask(__name__)

def checkAuth(args):
  # TODO: question - WebAPI works even when providing two Client ID's or two Users, why bother checking?
  # check if Client ID is provided, and only one provided
  if not args.has_key('client'):
    return ["bad", {"RESPONSE":"Input error", "MESSAGE":"No Client ID"}]
  elif len(args.to_dict(False)['client']) > 1:
    return ["bad", {"RESPONSE":"Input error", "MESSAGE":"Multiple Client ID's provided"}]
  # check if User is provided, and only one provided
  if not args.has_key('user'):
    return ["bad", {"RESPONSE":"Input error", "MESSAGE":"No User ID"}]
  elif len(args.to_dict(False)['user']) > 1:
    return ["bad", {"RESPONSE":"Input error", "MESSAGE":"Multiple User ID's provided"}]
  
  return ["good"]

def convertInputArgsToJSON(args):
  # convert input arguments into JSON format
  # lowercase all keys, and if a parameter is provided more than once, only get the first value
  # ex. ...&artist=The Beatles&artist=Jason Mraz, will only grab 'The Beatles'
  input_JSON = {}
  for key in request.args.keys():
    input_JSON[key.lower()] = request.args.get(key)
  return input_JSON

def checkInput(api="", input_JSON={}):
  # check if user provide correct input parameters 
  requiredParam = []
  # FOR DEVELOPMENT USE
  if api == "/search":
    requiredParam = ['artist', 'gender', 'fake_third_param']
    if not set(requiredParam) & set(input_JSON.keys()):
      return "<pre>You need to provide at least one of the three search text - artist, artist title or track title</pre>"
    
  elif api == "/album_search":
    requiredParam = ['artist', 'artist_title', 'track_title']
    if not set(requiredParam) & set(input_JSON.keys()):
      return ["bad", {"RESPONSE":"Missing query string", "MESSAGE":"Please provide at least one of the three search field - artist, artist title or track title"}]
  
  elif api == "/album_fingerprint":
    # TODO: develop a way to check required input for fingerprint lookup
    requiredParam = ['fingerprint']
    return ["bad", {"RESPONSE":"API under development", "MESSAGE":"This wrapper currently does not support this API call"}]
  
  elif api == "/album_toc":
    requiredParam = ['toc']
    if not set(requiredParam) & set(input_JSON.keys()):
      return ["bad", {"RESPONSE":"Missing query string", "MESSAGE":"Missing album TOC for ALBUM_TOC lookup"}]
  
  elif api == "/album_fetch":
    requiredParam = ['gn_id']
    if not set(requiredParam) & set(input_JSON.keys()):
      return ["bad", {"RESPONSE":"Missing query string", "MESSAGE":"Missing GN_ID to proceed ALBUM_FETCH lookup"}]
  
  else:
    return ["bad", {"RESPONSE":"NO CAES MATCHED ERROR", "MESSAGE":"Not matching any input check condition, check your code!"}]
  
  for param in requiredParam:
    if param not in input_JSON.keys():
      input_JSON[param] = ""
  
  return ["good"]

def createHTML(response):
  resultPage = open('templates/test.html', 'w')
  resultPage.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><title>Interactive Rhythm API Console</title></head><body><pre>' + response + '</pre></body></html>')
  resultPage.close()
  return "A HTML page to display returned JSON"

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/register")
def registerUser():
  auth_Check_Result = checkAuth(request.args)
  if auth_Check_Result[0] == "bad" and "No User ID" in auth_Check_Result[1]["MESSAGE"]:
    #return request.args.get('client')
    # TODO: potential issue, query will still go through if user is doing a search but forget to change the API/path/end point
    resultDOM = register(request.args.get('client'))
    response = resultDOM.getElementsByTagName("RESPONSE")[0]
    jsonResponse = getNodeContent(response)
    return "<pre>" + json.dumps(jsonResponse, sort_keys=True, separators=(',', ': ')) + "</pre>"
  else:
    return '<pre>{"RESPONSE":"Input error", "MESSAGE":"Please provide Client ID only"}</pre>'

@app.route("/index")
def sample():
  # TODO: FOR DEVELOPMENT USE ONLY
  auth_Check_Result = checkAuth(request.args)
  if auth_Check_Result[0] == "bad":
    return "<pre>" + json.dumps(auth_Check_Result[1], separators=(',', ': ')) + "</pre>"
  
  #response = "SEARCH<br>" + str(request.args)
  response = "SEARCH" + "<br>get " + str(request.args.get('client')) + "<br>keys " + str(request.args.keys()) + "<br>lists " + str(request.args.lists()) + "<br>listvalues " + str(request.args.listvalues()) + "<br>to_dict " + str(request.args.to_dict(False)) + "<br>viewitems " + str(request.args.viewitems()) + "<br>viewkeys " + str(request.args.viewkeys())
  if 'client' in request.args.keys():
    message = "<br>client id is provided"
    response += message
  return "<pre>" + response + "</pre>"

@app.route("/search")
def dev():
  auth_Check_Result = checkAuth(request.args)
  if auth_Check_Result[0] == "bad":
    return "<pre>" + json.dumps(auth_Check_Result[1], separators=(',', ': ')) + "</pre>"
  
  input_JSON = convertInputArgsToJSON(request.args)
  input_Check_Result = checkInput((request.path), input_JSON)
  if input_Check_Result[0] == "bad":
    return "<pre>" + json.dumps(input_Check_Result[1], separators=(',', ': ')) + "</pre>"
  return "<pre>" + request.path + " API<br>" + json.dumps(input_JSON, sort_keys=True, separators=(',', ': ')) + "</pre>"
  
  """
  # get metadata by calling getNodeContent function
  input = request.args.to_dict(False)
  resultDOM = search(clientID=input['client'][0], userID=input['user'][0], artist=input['ARTIST'][0])
  jsonResponse = {}
  response = resultDOM.getElementsByTagName("RESPONSE")[0]
  jsonResponse = getNodeContent(response)
  #return json.dumps(jsonResponse, sort_keys=True, separators=(',', ': '))
  
  # render returned metadata into an HTML output, trying to format JSON
  createHTML(json.dumps(jsonResponse, sort_keys=True, separators=(',', ': ')))
  return render_template('test.html')
  """

@app.route("/album_search")
def albumSearch():
  if request.args:
    response = "ALBUM_SEARCH with input(s)<br>" + str(request.args)
  else:
    response = "ALBUM_SEARCH"
  return response

@app.route("/album_fingerprint")
def albumFingerprint():
  if request.args:
    response = "ALBUM_FINGERPRINT with input(s)<br>" + str(request.args)
  else:
    response = "ALBUM_FINGERPRINT"
  return response

@app.route("/album_toc")
def albumToc():
  if request.args:
    response = "ALBUM_TOC with input(s)<br>" + str(request.args)
  else:
    response = "ALBUM_TOC"
  return response

@app.route("/album_fetch")
def albumFetch():
  if request.args:
    response = "ALBUM_FETCH with input(s)<br>" + str(request.args)
  else:
    response = "ALBUM_FETCH"
  return response

if __name__ == "__main__":
  app.debug = True
  app.run()