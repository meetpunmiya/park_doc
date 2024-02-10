# from flask import Flask, render_template, request
# import requests
# import time, datetime

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         return render_template('index.html', error='No file part')
#     file = request.files['file']
#     if file.filename == '':
#         return render_template('index.html', error='No selected file')
#     api_key = '33784bb65249af222949eee9998cabc54e9a5fce'
#     url = 'https://api.platerecognizer.com/v1/plate-reader/'
#     files = {'upload': file.read()}
#     headers = {'Authorization': f'Token {api_key}'}
#     response = requests.post(url, files=files, headers=headers)
#     result = response.json()
#     if 'results' in result and result['results']:
#         plate_info = result['results'][0]['plate']
#         time = datetime.datetime
#         ret = {'plate_info': plate_info, 'time': time}  
#     else:
#         plate_info = 'No license plate detected.'
#     return render_template('result.html', ret=ret)

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request
import requests
from datetime import date, datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    api_key = '33784bb65249af222949eee9998cabc54e9a5fce'
    url = 'https://api.platerecognizer.com/v1/plate-reader/'
    files = {'upload': file.read()}
    headers = {'Authorization': f'Token {api_key}'}

    try:
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        result = response.json()

        ret = {'plate_info': 'No license plate detected.',
               'date': date.today().strftime('%Y-%m-%d'),
               'time': datetime.now().strftime('%H:%M:%S')}

        if 'results' in result and result['results']:
            plate_info = result['results'][0].get('plate', 'N/A')
            ret['plate_info'] = plate_info

        return render_template('result.html', ret=ret)

    except requests.RequestException as e:
        # Handle request exceptions (e.g., network errors, timeouts)
        error_message = f"Error: {str(e)}"
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)


# aws s3 image uploa
# save the generated url in the database 
    #
    