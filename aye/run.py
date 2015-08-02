from flask import Flask, request, jsonify, abort
import psycopg2
import psycopg2.extras
import sys

from CustomParser import ConfigReader

app = Flask(__name__)

config_reader = ConfigReader('aye/config.ini')

state = 'Prod' if sys.argv[1] == 'prod' else 'Dev'

config_params = config_reader.get_config_section_map(state)

db_string = 'dbname=%s user=%s' % (config_params['db_name'],
                                   config_params['db_user'])

# Connect to an existing database
conn = psycopg2.connect(db_string,
                        cursor_factory=psycopg2.extras.RealDictCursor)

REQUIRED_CREATION_FIELDS = ['event_name', 'event_description', 'longitude',
                            'latitude']

REQUIRED_LOOKUP_FIELDS = ['longitude', 'latitude', 'distance']


@app.route('/new_event', methods=['GET', 'POST'])
def add_event():
    print "incoming!"
    if request.method == 'POST':
        try:
            data_dict = request.get_json()
            print data_dict
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

        except BadRequest:
            print "JSON parse error"
            # Bad Request
            abort(400)

        query_dict = {}

        for key in REQUIRED_LOOKUP_FIELDS:
            if key not in data_dict:
                abort(400)
            query_dict[key] = data_dict[key]

        try:
            cur = conn.cursor()

            cur.execute("select title, descr, longitude, latitude, \
                        ST_Distance(meter_point, \
                            ST_TRANSFORM(ST_SetSRID(ST_MAKEPOINT(%(longitude)s,%(latitude)s),4269),32661)) as distance \
                        from events where ST_DWithin(meter_point,\
                            ST_TRANSFORM(ST_SetSRID(ST_MAKEPOINT(%(longitude)s,%(latitude)s),4269),32661),\
                            %(distance)s)\
                        ORDER BY distance",
                        query_dict)

            events_in_radius = cur.fetchall()
            return_obj = {}
            return_obj['results'] = events_in_radius
            # return "ok"
            return jsonify(**return_obj)
        except:
            print "DB Error"
            abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
