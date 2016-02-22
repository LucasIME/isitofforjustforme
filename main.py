from flask import Flask, render_template, request
import re
from google.appengine.api import urlfetch
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/check', methods=['POST'])
def checkWebSite():
    if request.method == 'POST':
        url = request.form['webSiteUrl']
        url, isValid = valid(url)
        if isValid:
            try:
                response = urlfetch.fetch(url, method=urlfetch.HEAD)
                statusCode = response.status_code
            except:
                return render_template("error.html", message="Sorry, there was an error processing your URL")
            if validResponseCode(statusCode):
                return render_template('success.html', url= url)
            else:
                return render_template('fail.html', url= url)
        else:
            return render_template('error.html', message='Invalid URL')

def valid(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    validUrlPattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(validUrlPattern, url):
        return (url, True)
    else:
        return (url, False)

def validResponseCode( responseCode):
    if responseCode == 200 or responseCode == 301 or responseCode ==302:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run()
