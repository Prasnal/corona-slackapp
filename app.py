from flask import Flask
from flask import request, Response, jsonify

import requests

app = Flask(__name__)


def error_response(text):
    response = {
        "text": f'_{text}_'
    }

    return jsonify(response)


@app.route('/api/corona', methods=['POST'])
def slack_corona():

    if request.method == 'POST':
        param = request.form['text']

        if not param:
            return error_response("Please add country argument")

        url = f'https://coronavirus-19-api.herokuapp.com/countries/{param}'
        r = requests.get(url)

        if 'Country not found' in r.text:
            return error_response(f"Country *{param}* doesn't exist")

        try:
            results = r.json()
        except ValueError as e:
            return error_response("Ooops! Something went wrong, please try one more time.")
        try:
            validated_results = {
                'Country': results['country'],
                'Cases per one million': results['casesPerOneMillion'],
                'Today cases': results['todayCases'],
                'Today deaths': results['todayDeaths'],
                'Active': results['active'],
                'Critical': results['critical'],
                'All cases': results['cases'],
                'All deaths': results['deaths'],
                'Recovered': results['recovered']
            }
        except KeyError as e:
            return error_response("Ooops - seems that something is wrong with the API! Please report the issue.")

        my_str = ''.join(['*%s*: %s \n ' % (key, value) for (key, value) in validated_results.items()])

        response = {
            "response_type": "in_channel",
            "text": my_str
        }

        return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

