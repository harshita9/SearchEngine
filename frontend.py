from bottle import *
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
import redis
import json
import yaml
import ast
from autocorrect import spell

#-------------------- Beaker Stuff ---------------------------------------------
import bottle
from beaker.middleware import SessionMiddleware

# get info from backend
read_file = open('dump.json', 'r')
data = json.load(read_file)
read_file.close()

# extract data
page_ranks = data[0]['pageranks']
inverted_index = data[0]['invertedIndex']
document_index = data[0]['documentIndex']
lexicons = data[0]['lexicon']
url_titles = data[0]['titles']
url_paragraphs = data[0]['paragraphs']
inverted_index = inverted_index.replace("set(", "")
inverted_index = inverted_index.replace(")", "")
url_paragraphs = url_paragraphs.replace("\\n","")
url_paragraphs = url_paragraphs.replace("\\r","")

lexicons = yaml.load(lexicons)
url_titles = ast.literal_eval(url_titles)
inverted_index = ast.literal_eval(inverted_index)
document_index = ast.literal_eval(document_index)
page_ranks = ast.literal_eval(page_ranks)
url_paragraphs = ast.literal_eval(url_paragraphs)

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True
}

#request handler
sessionApp = SessionMiddleware(bottle.app(), session_opts)
#-------------------Beaker End--------------------------------------------------

##-------------GLOBAL VARIABLES FOR HOMEPAGE----------------------------------##
history_counter = """ """
word_counter = """ """
history = dict()
query = ""
pageranked_urls = []
pageranked_titles = {}
PER_PAGE = 5
num_pages = 1

## ---------------------------------------------------------------------------##

#------------------- R O U T E S ----------------------------------------------#
#------------------------------------------------------------------------------#
@route('/', 'GET')
def homepage():
    output = 0
    session = request.environ.get('beaker.session')
    print (session)

    try: # Check logged in info
        email = session['email']
        profilePicture = session['picture']
        userName = session['name']
        output = template('homepage.tpl', history = "Top 20 Words", table = history_counter, profilePicture = profilePicture , Name = userName, Email = email)
    except: # runs if no login info
        output = template('homepageanon.tpl')

    return output

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@error(404)
def error404(error):
    output = template('error.tpl')
    return output

@route('/search', method='POST')
def search_keyword():

    # get input string/keywords
    global query
    query = request.forms.get("keywords")
    query_lower = query.lower()

    # split the string and create a list of all words in string
    word_list = query_lower.split(" ")
    word_list_original = query.split(" ")

    # spell correction
    correct_word_list = []
    spell_correct = True
    for word in word_list_original:
        if spell(word) != word:
            word = spell(word)
            spell_correct = False
        correct_word_list.append(word)
    if not spell_correct:
        word_list = []
        query = ""
        n = 0
        for word in correct_word_list:
            word_list.append(word)
            if n != len(correct_word_list) - 1:
                query += word + " "
            else:
                query += word
            n += 1

    global lexicons
    global inverted_index
    global document_index
    global page_ranks
    global url_titles

    # get search results
    # multi word searching
    key_words1 = word_list
    key_words = []
    urls = []
    global pageranked_urls
    pageranked_urls = []
    global pageranked_titles
    global url_paragraphs
    pageranked_titles = {}

    for key_word1 in key_words1:
        key_word = "u'" + key_word1 + "'"
        key_words.append(key_word)

    for key_word in key_words:
        if key_word in lexicons:
            key_word_value = lexicons[key_word]
            url_id_list = inverted_index[key_word_value]

            for url, url_id in document_index.items():
                if url_id in url_id_list:
                    urls.append(url)

    if len(urls) != 0:
        for pr, rank in page_ranks:
            if pr in urls:
                try:
                    pageranked_titles[pr] = url_titles[str(pr)]
                    pageranked_urls.append(pr)
                except:
                    pageranked_titles[pr] = pr

                if pr not in url_paragraphs:
                    url_paragraphs[pr] = ""

    global num_pages
    if len(pageranked_urls) % 5 == 0:
        num_pages = int(len(pageranked_urls)/5)
    else:
        num_pages = int(len(pageranked_urls)/5) + 1

    d = dict()
    global history
    global word_counter
    # stores word count and word history in dictionaries
    for word in word_list:
        d[word] = d.get(word, 0) + 1
        history[word] = history.get(word, 0) + 1
    # list of words storted in descending order based on values
    new_history = sorted(history, key=history.get, reverse=True)
    # word count html table
    word_counter = """<table class="table table-bordered one-edge-shadow" name = /"results/"> <tr> <th>Word</th> <th>Count</th> </tr>"""
    # updating word history html table
    global history_counter
    history_counter = """<table class="table table-bordered one-edge-shadow" name = /"history/"> <tr> <th>Word</th> <th>Count</th> </tr>"""
    # updating word count table
    key_list = d.keys()
    count = 0
    for key in key_list:
        word_counter += ("<tr><td>" + key + "</td><td>" + str(d[key]) + "</td></tr>")
        count += 1
    if count == 1:
        word_counter = """ """
    # updating word history html table with top 20 keywords
    count = 0
    for key in new_history:
        if count == 20:
            break
        history_counter += ("<tr><td>" + key + "</td><td>" + str(history[key]) + "</td></tr>")
        count += 1

    redirect("/search/1")

@route("/search/<page>")
def pagination(page = '1'):

    global history_counter
    global word_counter
    global pageranked_urls
    global pageranked_titles
    global query
    global url_paragraphs
    global num_pages

    page = int(page)

    # create pages
    global PER_PAGE
    start = (page - 1) * PER_PAGE
    end = page * PER_PAGE

    parameters = {
            'page': page,
            'pageranked_urls': pageranked_urls,
            'start': start,
            'end': end,
            'pageranked_titles': pageranked_titles,
            'url_paragraphs': url_paragraphs,
            'num_pages': num_pages,
            }

    session = request.environ.get('beaker.session')
    output = 0;
    
    # Check logged in info
    try:
        profilePicture = session['picture']
        userName = session['name']
        email = session['email']
        output = template('pagination.tpl', key_word = query, profilePicture = profilePicture, Name = userName, Email = email, **parameters)
    except: # runs if no login info
        output = template('paginationAnon.tpl', key_word = query, **parameters)
    return output

@route('/login')
def logIn():
    flow = flow_from_clientsecrets("LOLUWISH")
    uri = flow.step1_get_authorize_url()
    redirect(str(uri))

@route('/redirect')
def redirect_page():
    code = request.query.get('code','')
    flow = OAuth2WebServerFlow(client_id="LOLUWISH", client_secret = "LOLUWISH", scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', redirect_uri = "http://localhost:8080/redirect")
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']

    http = httplib2.Http()
    http = credentials.authorize(http)

    #get user email
    users_service = build('oauth2','v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']

    saveSession(user_document)
    # after successfully entering information, redirect to the home page
    redirect('/')

@route('/logout')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    redirect('/')

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
## ------Functions-------------------------------------------------------------
#Function saves the session information
def saveSession(user_document):
        #save session
        print (user_document) # checks the keys for user doc
        session = request.environ.get('beaker.session')
        try:
            if user_document['name'] is '':
                session['name'] = 'Acrobatic Armadillo'
            else:
                session['name'] = user_document['name']
        except:
            session['name'] = ""
        try:
            session['email'] = user_email
        except:
            session['email'] = ""
        try:
            session['picture'] = user_document['picture']
        except:
            session['picture'] = "https://images.pexels.com/photos/356378/pexels-photo-356378.jpeg?auto=compress&cs=tinysrgb&h=350"

        session.save()
        print ("/redirect: session ", session)



#run the app
bottle.run(app=sessionApp)
#bottle.run(host = "0.0.0.0", port = 80)
