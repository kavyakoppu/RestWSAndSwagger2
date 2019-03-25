import csv, logging, json, random, os
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, make_response, jsonify
app = Flask(__name__, template_folder='HTML')

app.static_folder = 'static'

def validateDate(inputDate):
    ValidDate = False
    try:
        inputDate = datetime.strptime(inputDate, "%Y%m%d").date()
        ValidDate = True
    except ValueError:
        ValidDate = False
    return ValidDate

@app.route('/', methods=['GET','POST'])
def index():
    # return render_template('index.html')
    home = "Check Weather Information using the following Resources: \n/historical/ - GET, POST\n/historical/[date] - GET, DELETE\n/forecast/[date] - GET\n"
    return home

@app.route('/historical/', methods=['GET'])
def getAvaliableHistoricalData():
    # if request.method == 'GET':
    dates = []
    with open('dailyweather.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        for row in csv_reader:
            datefield = {"DATE":  row[0]}
            dates.append(datefield)
        dates.pop(0)
        # return json.dumps(dates)
        return make_response(jsonify(dates), 200)

@app.route('/historical/<inputDate>', methods=['GET'])
def gethistoricalDataOfADate(inputDate):
    if validateDate(inputDate) :
        data = []
        with open('dailyweather.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if(row[0] == inputDate):
                    data = {"DATE":  row[0], "TMAX": row[1], "TMIN": row[2]}
                    return make_response(jsonify(data), 200)
        return make_response(jsonify({'error' : 'Date Not found'}), 404)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

@app.route('/historical/', methods=['POST'])
def addHistoricalData():
    print(request.data)
    reqBodyData = json.loads(request.data)
    if validateDate(reqBodyData["DATE"]) :
        deleteHistoricalDataOfADate(reqBodyData["DATE"])
        outputFile = open('dailyweather.csv', 'a')
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow([reqBodyData["DATE"], reqBodyData["TMAX"], reqBodyData["TMIN"]])
        return make_response(jsonify({'DATE' : reqBodyData["DATE"]}), 201)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

@app.route('/historical/<inputDate>', methods=['DELETE'])
def deleteHistoricalDataOfADate(inputDate):
    existing = False
    if validateDate(inputDate) :
        with open('dailyweather.csv', 'r') as inp, open('dailyweathercopy.csv', 'w') as temp:
            writer = csv.writer(temp)
            for row in csv.reader(inp):
                if row[0] != inputDate:
                    writer.writerow(row)
                else:
                    existing = True   
        os.remove('dailyweather.csv')
        os.rename('dailyweathercopy.csv', 'dailyweather.csv')
        if existing :
            return make_response(inputDate, 204)
        else :
            return make_response(jsonify({'error' : 'Date Not found'}), 404)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

@app.route('/forecast/<inputDate>', methods=['GET'])
def getForecastForAWeek(inputDate):
    if validateDate(inputDate) :
        forecast = []
        existing = False
        sampleMAXData = [60.11, 58.75, 54, 57.5, 70.5, 71.6, 61.2, 72.9, 68.2, 71.1, 72.5, 58.7, 72.3, 77.9]
        sampleMINData = [58.25, 51.2, 51.75, 52.5, 62.4, 66.3, 59.3, 69.1, 65.4, 62.3, 56.4, 52, 65, 68.7]
        with open('dailyweather.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i in range(7):
                existing = False
                for row in csv_reader:
                    if(row[0] == inputDate):
                        data = {"DATE":  row[0], "TMAX": row[1], "TMIN": row[2]}
                        forecast.append(data)
                        existing = True
                        break
                if not existing :
                    index = random.randint(0,13)
                    data = {"DATE":  inputDate, "TMAX": sampleMAXData[index], "TMIN": sampleMINData[index]}
                    forecast.append(data)
                # inputdate++
                tempDate = datetime.strptime(inputDate, "%Y%m%d").date()
                tempDate += timedelta(days=1)
                inputDate = tempDate.strftime("%Y%m%d")
        return make_response(jsonify(forecast), 200)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

# abort(400)
@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
# make_response(jsonify({'error': 'Method Not Found'}), 405)
def methodNotFound(error):
    return index()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)