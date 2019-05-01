wget -nc http://data.cquest.org/dgac/restrictions_drones/restrictions_drones_201811.json.gz
ogr2ogr -f postgresql PG:"dbname=$USER" -nln drones -nlt geometry /vsigzip/restrictions_drones_201811.json.gz
psql -c "
-- nettoyage
ALTER TABLE drones DROP ogc_fid;
ALTER TABLE drones DROP fid;
-- retypage
ALTER TABLE drones ALTER limite type integer USING limite::integer;
-- renommage
ALTER TABLE drones RENAME wkb_geometry TO geom;
-- correction géométries invalides
UPDATE drones SET geom = ST_MakeValid(geom) WHERE NOT ST_IsValid(geom);

"

# génération des polygones de limite à 150m (hors zones de restriction)
wget -nc http://osm13.openstreetmap.fr/~cquest/openfla/departements-20180101-simplifies.json.gz
ogr2ogr -f postgresql PG:"dbname=$USER" -nln departements_simplifies -nlt geometry /vsigzip/departements-20180101-simplifies.json.gz
psql -c "
INSERT INTO drones
  SELECT
    150 as limite,
    st_difference(wkb_geometry,(select st_unaryunion(st_collect(st_intersection(wkb_geometry,geom))) from drones where wkb_geometry && geom)) as geom
  from
    departements_simplifies
  where code_insee <= '95'
  group by code_insee, wkb_geometry;
"
