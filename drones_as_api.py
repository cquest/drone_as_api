#! /usr/bin/python3

# modules additionnels
import falcon
import psycopg2

class dgac_drone(object):
    def getDrone(self, req, resp):
        db = psycopg2.connect("")  # connexion à la base PG locale
        cur = db.cursor()

        where = ''

        lat = float(req.params.get('lat', None).replace(',','.'))
        lon = float(req.params.get('lon', None).replace(',', '.'))
        dist=min(int(req.params.get('rayon', 1000)), 10000)

        limite = req.params.get('limite', None)
        if limite:
            where = where + cur.mogrify(" AND limite >= %s", (limite,)).decode()

        if lat and lon:  # recherche géographique
            query = """
select json_build_object('source', 'DGAC / SIA',
    'derniere_maj', '2018-11',
    'type','Featurecollection',
    'nb_features', count(d.*),
    'features', case when count(*)=0 then array[]::json[] else array_agg(json_build_object(
        'type','Feature',
            'properties',json_build_object(
                'limite_alti_m', limite,
                'distance_m', ST_Distance(geom::geography,st_setsrid(st_makepoint(%(lon)s, %(lat)s),4326)::geography)::int,
                'cap_deg', case when ST_Distance(geom::geography,st_setsrid(st_makepoint(%(lon)s, %(lat)s),4326)::geography)>0
                    then degrees(ST_Azimuth(st_setsrid(st_makepoint(%(lon)s, %(lat)s),4326), ST_ClosestPoint(geom, st_setsrid(st_makepoint(%(lon)s, %(lat)s),4326))))::int
                    else null end
            ),
            'geometry',st_asgeojson(geom,6,0)::json)
            order by ST_Distance(geom::geography,st_setsrid(st_makepoint(%(lon)s, %(lat)s),4326)::geography)
        ) end )::text
from drones d
where st_buffer(st_setsrid(st_makepoint(%(lon)s, %(lat)s),4326)::geography, %(dist)s)::geometry && geom
    and ST_DWithin(st_setsrid(st_makepoint(%(lon)s, %(lat)s),4326)::geography, geom::geography,  %(dist)s)
""" % {'lon': lon, 'lat': lat, 'dist': dist} + where

            print(query)
            cur.execute(query)
            drones = cur.fetchone()

            resp.status = falcon.HTTP_200
            resp.set_header('X-Powered-By', 'drone_as_api (https://github.com/cquest/drone_as_api/)')
            resp.set_header('Access-Control-Allow-Origin', '*')
            resp.set_header("Access-Control-Expose-Headers","Access-Control-Allow-Origin")
            resp.set_header('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept')
            resp.body = drones[0]
        else:
            resp.status = falcon.HTTP_413
            resp.body = '{"erreur": "aucun critère de recherche indiqué"}'

        db.close()

    def on_get(self, req, resp):
        self.getDrone(req, resp);

# instance WSGI et route vers notre API
app = falcon.API()
app.add_route('/drone', dgac_drone())
