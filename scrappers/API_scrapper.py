from flask import Flask, request
import jsonpickle
from scrappers.constants_scrappers import Constants, TimeRange
import time
from scrappers.Utils import download_files, load_browser, scrap_web

app = Flask(__name__)


@app.route('/download_files', methods=['POST'])
def api_download_files():
    if request.method == 'POST':
        data = jsonpickle.decode(request.data)
        try:
            companies = data["companies"]
            download_files(companies, TimeRange.MAX)
            response = jsonpickle.encode(companies)
        except Exception as error:
            response = error
        return response
    else:
        return 'POST method. Ex: {companies : ["aapl", "amzn", "tsla"]}'


@app.route('/launch_scrapper', methods=['POST'])
def launch_scrapper():
    try:
        browser = load_browser()
        while True:  # Don't close the browser
            response = scrap_web(browser)
            # -----------> KAFKA connected with the json_response
            time.sleep(Constants.FREQUENCY_SCRAPPING_MS / 1000)
        # browser.quit()
    except Exception as error:
        response = error
    return response


@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


if __name__ == "__main__":
    app.run(debug=True)




