from flask import Flask, jsonify
from datetime import date, timedelta, datetime
import requests

app = Flask(__name__)
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSTUIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk2MDE4LCJpYXQiOjE2NjA3NjAwMTh9.Ud4qSIXGglbXaYeK-JDzL9GolEskKk9aCGrl79NMDY4'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSRFQiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkzNDg4MDQxLCJpYXQiOjE2NjE5NTIwNDF9.uk4UyLwyQeLjnoE6jxKPNCxfkzs0mFTq_09cfuyV74U'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSNkIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk1NDQ0LCJpYXQiOjE2NjA3NTk0NDR9.bILcGIrPRXPWRrWBZDKRLsZdtTKKqPUpZ4NZZ-U3k5g'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRNVIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIxOTk2LCJpYXQiOjE2NjA3ODU5OTZ9.Rw2SpXEMA3YVx1-O1W0ZamKq2BwRnUpOw_fQCMRn0z8'}
myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRUEYiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIyMTc4LCJpYXQiOjE2NjA3ODYxNzh9.t4-tjP-pBKe-wdbYLTL9t-h7wAOWsAlu-cGurSkfJiU'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRTkQiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIyMzQ0LCJpYXQiOjE2NjA3ODYzNDR9.-kAqRq3x5D5J0nCgzOm-2ATMbz9e7EZYXUiitEt6h4k'}


@app.route("/heartrate/last", methods=["GET"])
def get_heart_rate():
    # Return the most recent heartrate.
    dayinput = date.today()
    myurl = "https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d.json".format(
        dayinput)
    resp = requests.get(myurl, headers=myheader).json()
    activity_dataset = resp["activities-heart-intraday"]["dataset"]
    while (len(activity_dataset) == 0):
        # if there is no data on that day, check the previous days.
        dayinput -= timedelta(days=1)
        myurl = "https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d.json".format(
            dayinput)
        resp = requests.get(myurl, headers=myheader).json()
        activity_dataset = resp["activities-heart-intraday"]["dataset"]
    recent = activity_dataset[-1]
    # retrieve heartrate, timeoffset (min)
    heartrate = recent["value"]
    timeoffset = datetime.now() - datetime.combine(dayinput, datetime.strptime(
        recent["time"], "%H:%M:%S").time())
    ret = {"heart-rate": heartrate, "time offset": timeoffset.seconds//60}
    return jsonify(ret)


@app.route("/steps/last", methods=["GET"])
def get_steps():
    # Return the most recent step.
    dayinput = date.today()
    myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json"
    resp = requests.get(myurl, headers=myheader).json()
    activity_step = resp["activities-steps"]
    timeoffset = resp["activities-steps-intraday"]["datasetInterval"]
    myurl = "https://api.fitbit.com/1/user/-/activities/distance/date/today/1d.json"
    resp = requests.get(myurl, headers=myheader).json()
    activity_distance = resp["activities-distance"]
    while (len(activity_step) == 0 or len(activity_distance) == 0):
        # if there is no data on that day, check the previous days.
        dayinput -= timedelta(days=1)
        myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/{}/1d.json".format(
            dayinput)
        resp = requests.get(myurl, headers=myheader).json()
        activity_step = resp["activities-steps"]
        myurl = "https://api.fitbit.com/1/user/-/activities/distance/date/{}/1d.json".format(
            dayinput)
        resp = requests.get(myurl, headers=myheader).json()
        activity_distance = resp["activities-distance"]
    timeoffset = datetime.now() - datetime.combine(dayinput, datetime.min.time())
    ret = {"step-count": activity_step[-1]["value"],
           "distance": activity_distance[-1]["value"], "time offset": timeoffset.seconds//60}
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
