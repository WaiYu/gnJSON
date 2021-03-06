from flask import Flask
from flask import request, render_template, jsonify
import json
from pygn2 import register, search, fingerprint, fetch, getNodeContent
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

def checkRequiredParam(api="", input_JSON={}):
  # check if user provide correct input parameters 
  requiredParam = []
  if api == "/album_search":
    requiredParam = ['artist', 'album_title', 'track_title']
    if not set(requiredParam) & set(input_JSON.keys()):
      return ["bad", {"RESPONSE":"Missing query string", "MESSAGE":"Please provide at least one of the three search field - artist, artist title or track title"}]
  
  elif api == "/album_fingerprint":
    requiredParam = ['fingertprint_algorithm', 'version', 'data']
    if not set(requiredParam) & set(input_JSON.keys()) == set(requiredParam):
      return ["bad", {"RESPONSE":"Missing required query information", "MESSAGE":"Please provide all required fields - fingertprint_algorithm, version and data"}]
  
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
  
  return ["good", input_JSON]

def checkInput(request):
  auth_Check_Result = checkAuth(request.args)
  if auth_Check_Result[0] == "bad":
    return auth_Check_Result
  
  input_JSON = convertInputArgsToJSON(request.args)
  input_Check_Result = checkRequiredParam((request.path), input_JSON)
  if input_Check_Result[0] == "bad":
    return input_Check_Result
  return input_Check_Result

@app.route("/")
def hello():
  return render_template('index.html')
  return "This is the Gracenote WebAPI wrapper - a RESTful API interface"

@app.route("/register")
def registerUser():
  auth_Check_Result = checkAuth(request.args)
  if auth_Check_Result[0] == "bad" and "No User ID" in auth_Check_Result[1]["MESSAGE"]:
    # TODO: potential issue, query will still go through if user is doing a search but forget to change the API/path/end point
    resultDOM = register(request.args.get('client'))
    response = resultDOM.getElementsByTagName("RESPONSE")[0]
    jsonResponse = getNodeContent(response)
    return jsonify(jsonResponse)
  else:
    jsonResponse = {"RESPONSE":"Input error", "MESSAGE":"Please provide Client ID only"}
    return jsonify(jsonResponse)

@app.route("/index")
def sample():
  # TODO: FOR DEVELOPMENT USE ONLY
  auth_Check_Result = checkAuth(request.args)
  if auth_Check_Result[0] == "bad":
    return jsonify(auth_Check_Result[1])
  
  #response = "SEARCH<br>" + str(request.args)
  response = "SEARCH" + "<br>get " + str(request.args.get('client')) + "<br>keys " + str(request.args.keys()) + "<br>lists " + str(request.args.lists()) + "<br>listvalues " + str(request.args.listvalues()) + "<br>to_dict " + str(request.args.to_dict(False)) + "<br>viewitems " + str(request.args.viewitems()) + "<br>viewkeys " + str(request.args.viewkeys())
  if 'client' in request.args.keys():
    message = "<br>client id is provided"
    response += message
  return "<pre>" + response + "</pre>"

@app.route("/album_search")
def albumSearch():
  check_Result = checkInput(request)
  if check_Result[0] == "bad":
    return jsonify(check_Result[1])
  
  input_JSON = check_Result[1]
  # get metadata by calling getNodeContent function
  resultDOM = search(clientID=input_JSON['client'], userID=input_JSON['user'], artist=input_JSON['artist'], album=input_JSON['album_title'], track=input_JSON['track_title'], input_JSON=input_JSON)
  jsonResponse = {}
  response = resultDOM.getElementsByTagName("RESPONSE")[0]
  jsonResponse = getNodeContent(response)
  return jsonify(jsonResponse)

@app.route("/album_fingerprint")
def albumFingerprint():
  check_Result = checkInput(request)
  if check_Result[0] == "bad":
    return jsonify(check_Result[1])
  
  # temporarily disable album fingerprint look up, until this API function verified/tested
  jsonResponse = {"RESPONSE":"Wrapper error", "MESSAGE":"This API is currently under development, please use GNSDK for fingerprint lookup"}
  return jsonify(jsonResponse)
  
  input_JSON = check_Result[1]
  # get metadata by calling getNodeContent function
  resultDOM = fingerprint(clientID=input_JSON['client'], userID=input_JSON['user'], fingertprint_algorithm=input_JSON['fingertprint_algorithm'], version=input_JSON['version'], data=input_JSON['data'], input_JSON=input_JSON)
  jsonResponse = {}
  response = resultDOM.getElementsByTagName("RESPONSE")[0]
  jsonResponse = getNodeContent(response)
  return jsonify(jsonResponse)

@app.route("/album_toc")
def albumToc():
  check_Result = checkInput(request)
  if check_Result[0] == "bad":
    return jsonify(check_Result[1])
  
  input_JSON = check_Result[1]
  # get metadata by calling getNodeContent function
  resultDOM = search(clientID=input_JSON['client'], userID=input_JSON['user'], toc=input_JSON['toc'], input_JSON=input_JSON)
  jsonResponse = {}
  response = resultDOM.getElementsByTagName("RESPONSE")[0]
  jsonResponse = getNodeContent(response)
  return jsonify(jsonResponse)

@app.route("/album_fetch")
def albumFetch():
  check_Result = checkInput(request)
  if check_Result[0] == "bad":
    return jsonify(check_Result[1])
  
  input_JSON = check_Result[1]
  # get metadata by calling getNodeContent function
  resultDOM = fetch(clientID=input_JSON['client'], userID=input_JSON['user'], GNID=input_JSON['gn_id'], input_JSON=input_JSON)
  jsonResponse = {}
  response = resultDOM.getElementsByTagName("RESPONSE")[0]
  jsonResponse = getNodeContent(response)
  return jsonify(jsonResponse)

if __name__ == "__main__":
  app.debug = True
  app.run()