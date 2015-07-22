from flask import Flask, request, jsonify, abort
import psycopg2
import sys

app = Flask(__name__)


# Connect to an existing database
conn = psycopg2.connect("dbname=aye_test user=rohan")


REQUIRED_CREATION_FIELDS = ['event_name', 'event_description', 'longitude',
                            'latitude']

REQUIRED_LOOKUP_FIELDS = ['longitude', 'latitude', 'distance']


@app.route('/new_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        try:
            data_dict = request.get_json()
            table_data = {}

            for key in REQUIRED_CREATION_FIELDS:
                if key not in data_dict:
                    abort(400)
                table_data[key] = data_dict[key]

            cur = conn.cursor()
            cur.execute("INSERT INTO events(title,descr,longitude,latitude) \
                        VALUES (%(event_name)s,%(event_description)s, \
                        %(longitude)s,%(latitude)s)", table_data)
            conn.commit()

            return_obj = {}
            return_obj['message'] = "Event Created"

            return jsonify(**return_obj)

        except:
            e = sys.exc_info()[0]
            print "%s" % e


@app.route('/find_event', methods=['GET', 'POST'])
def find_event():
    if request.method == 'POST':
        try:
            data_dict = request.get_json()

            query_dict = {}

            for key in REQUIRED_LOOKUP_FIELDS:
                if key not in data_dict:
                    abort(400)
                query_dict[key] = data_dict[key]

            cur = conn.cursor()

            cur.execute("select * from events where \
                        ST_DWithin(meter_point,\
                            ST_TRANSFORM(\
                                        ST_SetSRID(ST_MAKEPOINT(%(longitude)s,%(latitude)s,%(distance)s),4269),\
                                        32661),\
                            206)",
                        query_dict)

            events_in_radius = cur.fetchall()
            return_obj = {}
            return_obj['results'] = events_in_radius
            # return "ok"
            return jsonify(**return_obj)
        except:
            print "Error"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
