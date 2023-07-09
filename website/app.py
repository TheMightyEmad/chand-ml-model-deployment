from flask import Flask, render_template, request, jsonify,send_file
import mysql.connector.pooling
from flask import Flask, request, render_template
import joblib
import numpy as np
import json
import re

app = Flask(__name__)

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_connection_pool",
    pool_size=5,
    host="localhost",
    user="root",
    password="admin",
    database="main_database"
)

with open('models/location_dict.json', 'r') as f:
    location_dict = json.load(f)
scaler_main=joblib.load('models/scaler_main.joblib')
scaler_price=joblib.load('models/scaler_price.joblib')

model = joblib.load('models/random_forrest_model.joblib')
model2 = joblib.load('models/desicion_tree_model.joblib')
model3 = joblib.load('models/gradient_boosting_model.joblib')

def persian_to_english(text):
    persian_numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    english_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(len(persian_numbers)):
        text = text.replace(persian_numbers[i], english_numbers[i])
    return text
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/image.png')
def get_buy_img():
    return send_file('templates/images/image.png', mimetype='image/x-png')
@app.route('/favicon-32x32.png')
def favicon():
    return send_file('templates/images/favicon-32x32.png', mimetype='image/x-png')
@app.route('/logo.png')
def get_logo():
    return send_file('templates/images/logo.png', mimetype='image/x-png')
@app.route('/IRANSansWeb.ttf')
def get_font():
    return send_file('IRANSansWeb.ttf', mimetype='font/ttf')
@app.route('/script.js')
def get_script():
    return send_file('templates/js/script.js', mimetype='text/javascript')
@app.route('/bootstrap.rtl.min.css')
def get_bootstrap_css():
    return send_file('templates/css/bootstrap.rtl.min.css', mimetype='text/css')
@app.route('/style.css')
def get_css():
    return send_file('templates/css/style.css', mimetype='text/css')
@app.route('/search')
def search():
    db=connection_pool.get_connection()
    query = request.args.get('query')
    query=persian_to_english(query)
    query = query.replace(' ','%')
    cursor = db.cursor()
    cursor.execute(f"SELECT model FROM dict_value WHERE model LIKE '%{query}%' LIMIT 4")
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()
    return jsonify(results)
@app.route('/get_years', methods=['POST'])
def get_years():
    db=connection_pool.get_connection()
    solar_years=[1370,1403]
    Gregorian_years=[1950,2024]
    selected_model = request.form['selectedModel']
    cursor = db.cursor()
    cursor.execute(f"SELECT year FROM dict_value WHERE model = '{selected_model}'")
    years_type = str(cursor.fetchall()[0][0])
    cursor.close()
    db.close()
    if years_type=='s':
        years=[i for i in range(solar_years[0],solar_years[1])]
    if years_type=='m':
        years=[i for i in range(Gregorian_years[0],Gregorian_years[1])]
    return jsonify(years)

@app.route('/predict',methods=['POST'])
def predict():
    #preprocess the inputs
    int_features = [str(x) for x in request.form.values()] 
    int_features[2]=persian_to_english(int_features[2])
    int_features[2]=re.findall(r"\d+", int_features[2])[0]
    int_features[1]=float(int_features[1])
    int_features[2]=float(int_features[2])
    #fetch the encoded value for the car
    db=connection_pool.get_connection()
    cursor = db.cursor()
    cursor.execute(f"SELECT encoded FROM dict_value WHERE model ='{int_features[0]}'")
    encoded_car=cursor.fetchall()[0]
    cursor.close()
    db.close()
    int_features[1]=float(int_features[1])
    #normalize the shamsi and georgian dates
    if int_features[1]<1500:int_features[1]+=621
    int_features[0]=float(encoded_car[0])
    #scale the values as scaled in jupyter
    int_features[1]=float(scaler_main.transform([[0, int_features[1]]])[0][1])
    int_features[2]=float(np.squeeze(scaler_main.transform([[int_features[2], 0]])[0][0]))
    if int_features[3] not in location_dict:
        average_value = sum(location_dict.values()) / len(location_dict)
        int_features[3] = average_value
    else:
        int_features[3] = float(location_dict[int_features[3]])
    features = [np.array(int_features)]  
    #predict the output
    scaled_number=np.squeeze(model.predict(features))
    exped=np.exp(scaled_number)
    #inverse the log function and scaling
    output1 = int(np.squeeze(scaler_price.inverse_transform(exped.reshape(1,-1))))
    scaled_number2=np.squeeze(model2.predict(features))
    exped2=np.exp(scaled_number2)
    output2 = int(np.squeeze(scaler_price.inverse_transform(exped2.reshape(1,-1))))
    scaled_number3=np.squeeze(model3.predict(features))
    exped3=np.exp(scaled_number3)
    output3 = int(np.squeeze(scaler_price.inverse_transform(exped3.reshape(1,-1))))
    #calculate the average between models
    output= (output1 + output2 + output3) / 3
    #round the price
    output = round(output / 1000000) * 1000000
    #give back to JS
    return json.dumps({'variable': output}, default=int)
if __name__ == '__main__':
    app.run()
