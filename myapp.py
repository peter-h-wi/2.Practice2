from flask import Flask, jsonify
from datetime import date, timedelta
import requests

app = Flask(__name__)
myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSTUIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk2MDE4LCJpYXQiOjE2NjA3NjAwMTh9.Ud4qSIXGglbXaYeK-JDzL9GolEskKk9aCGrl79NMDY4'}


@app.route("/heartrate/last", methods=["GET"])
def get_heart_rate():
    # Return the most recent heartrate.
    timeoffset = 15
    dayinput = date.today()
    myurl = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/{}min/time/00:00/23:59.json".format(
        timeoffset)
    resp = requests.get(myurl, headers=myheader).json()
    activity_dataset = resp["activities-heart-intraday"]["dataset"]
    while (len(activity_dataset) == 0):
        # if there is no data on that day, check the previous days.
        dayinput -= timedelta(days=1)
        myurl = "https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d/{}min/time/00:00/23:59.json".format(
            dayinput, timeoffset)
        resp = requests.get(myurl, headers=myheader).json()
        activity_dataset = resp["activities-heart-intraday"]["dataset"]
    recent = activity_dataset[-1]
    heartrate = recent["value"]
    ret = {"heart-rate": heartrate, "time offset": timeoffset}
    return jsonify(ret)


@app.route("/steps/last", methods=["GET"])
def get_steps():
    # Return the most recent step.
    timeoffset = 15
    dayinput = date.today()
    myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d/{}min.json".format(
        timeoffset)
    resp = requests.get(myurl, headers=myheader).json()
    activity_step = resp["activities-steps"]
    myurl = "https://api.fitbit.com/1/user/-/activities/distance/date/today/1d/{}min.json".format(
        timeoffset)
    resp = requests.get(myurl, headers=myheader).json()
    activity_distance = resp["activities-distance"]
    while (len(activity_step) == 0 or len(activity_distance) == 0):
        # if ther eis no data on that day, check the previous days.
        dayinput -= timedelta(days=1)
        myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/{}/1d/{}min.json".format(
            dayinput, timeoffset)
        resp = requests.get(myurl, headers=myheader).json()
        activity_step = resp["activities-steps"]
        myurl = "https://api.fitbit.com/1/user/-/activities/distance/date/{}/1d/{}min.json".format(
            dayinput, timeoffset)
        resp = requests.get(myurl, headers=myheader).json()
        activity_distance = resp["activities-distance"]
    ret = {"step-count": activity_step[-1]["value"],
           "distance": activity_distance[-1]["value"], "time offset": timeoffset}
    return jsonify(ret)


@app.route("/sleep/<date_input>", methods=["GET"])
def get_sleep(date_input):
    myurl = "https://api.fitbit.com/1.2/user/-/sleep/date/{}.json".format(
        date_input)
    resp = requests.get(myurl, headers=myheader).json()
    ret = {}
    if len(resp["sleep"]) > 0:
        sleep = resp["sleep"][0]["levels"]["summary"]
        for key in sleep:
            ret[key] = sleep[key]["minutes"]
    return ret


@app.route("/activity/<date_input>", methods=["GET"])
def get_activeness(date_input):
    # Return the activeness.
    myurl = "https://api.fitbit.com/1/user/-/activities/date/{}.json".format(
        date_input)

    resp = requests.get(myurl, headers=myheader).json()
    summary = resp["summary"]

    sedentary = summary["sedentaryMinutes"]
    lightly_active = summary["lightlyActiveMinutes"]
    fairly_active = summary["fairlyActiveMinutes"]
    very_active = summary["veryActiveMinutes"]

    ret = {"very-active": very_active, "fairly-active": fairly_active,
           "lightly-active": lightly_active, "sedentary": sedentary}
    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True)
