from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import json


def test(request):
    response = json.dumps({"test": "test"})
    return HttpResponse(response, content_type='text/json')

def test_with_var(request, test_var):
    if request.method == 'GET':
        response = json.dumps([{ 'test_var': test_var}])
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def aircraft(request, aircraftid):

    if request.method == 'GET':
        from factory import engine
        threshold=20
        aircrafts = engine.execute(
            '''select * from flotte where "Nom de l'appareil"=%(aircraftid)s''',
            {"aircraftid": aircraftid}
        ).fetchall()
        query = '''
            select RUL,ts
            from rultrack r
            where r.aircraftid=%(aircraftid)s
            order by ts asc
        '''
        aircraft_res = {}
        for aircraft in aircrafts:
            aircraftid = aircraft[2]
            aircraft_type = aircraft[1]
            res = engine.execute(query, {"aircraftid": aircraftid}).fetchall()
            ruls = [res[i][0] for i in range(len(res))]
            ts = [str(res[i][1]) for i in range(len(res))]
            if(len(res)==0):
                aircraft_res = {"name": aircraftid, "aircraft_type": aircraft_type, "status" : "undefined", "rul": [], "timeseries" : []}
            else:
                status= "healthy"
                if(ruls[-1]<threshold):
                    status="in danger"
                aircraft_res = {
                    "status": status,
                    "name": aircraftid,
                    "aircraft_type": aircraft_type,
                    "rul": ruls,
                    "timeseries": ts
                }
        return HttpResponse(json.dumps(aircraft_res), content_type='text/json')

    if request.method == 'POST':
        threshold=20
        from factory import predictive_maintenance_model
        from factory import engine
        import pandas as pd
        payload = json.loads(request.body)
        sensors = dict(payload)
        ts = datetime.datetime.strptime(payload["TimeStamp"], "%Y-%m-%d %H:%M:%S.%f")
        del sensors["TimeStamp"]
        df = pd.DataFrame([sensors])
        print(df)
        print(ts)

        RUL = predictive_maintenance_model.predict(df)[0]

        query='''
        INSERT INTO rultrack (aircraftid, rul, ts)
        VALUES (%(aircraftid)s, %(RUL)s, %(ts)s)
        '''
        engine.execute(query, {"aircraftid": aircraftid, "RUL": RUL, "ts": str(ts)})
        if (RUL<20):
            from utils.email import send_email
            send_email(aircraftid, RUL)
        return HttpResponse(json.dumps({"result" : True, "RUL": RUL, "aircraftid": aircraftid}), content_type='text/json') 

    if request.method == 'DELETE':
        from factory import engine
        try:
            query='''delete from rultrack where aircraftid=%(aircraftid)s'''
            engine.execute(query, {"aircraftid": aircraftid})
            return HttpResponse(json.dumps({"result": True}), content_type='text/json')
        except Exception as e:
            return HttpResponse(json.dumps({"result": False, "exception": str(e)}), content_type='text/json')


def aircrafts(request):

    if request.method=="GET":
        import datetime
        from factory import engine
        threshold=20
        aircrafts = engine.execute("select * from flotte").fetchall()
        query = '''
            select RUL,ts
            from rultrack r
            where r.aircraftid=%(aircraftid)s
            order by ts asc
        '''
        aircrafts_res = []
        for aircraft in aircrafts:
            aircraftid = aircraft[2]
            aircraft_type = aircraft[1]
            res = engine.execute(query, {"aircraftid": aircraftid}).fetchall()
            ruls = [res[i][0] for i in range(len(res))]
            ts = [str(res[i][1]) for i in range(len(res))]
            if(len(res)==0):
                aircrafts_res.append({"name": aircraftid, "aircraft_type": aircraft_type, "status" : "undefined", "rul": [], "timeseries" : []})
            else:
                status= "healthy"
                if(ruls[-1]<threshold):
                    status="in danger"
                aircraft_res = {
                    "status": status,
                    "name": aircraftid,
                    "aircraft_type": aircraft_type,
                    "rul": ruls,
                    "timeseries": ts
                }
                aircrafts_res.append(aircraft_res)
        return HttpResponse(json.dumps(aircrafts_res), content_type='text/json')


def flight(request, day=25, month=1, year=2020):

    if request.method=='GET':
        from utils.scraping import get_flights_realtime
        try :
            return get_flights_realtime(day, year, month)
        except Exception as e:
            import traceback
            return HttpResponse(json.dumps({"error": str(e), "stacktrace": traceback.format_exc()}), content_type='text/json')