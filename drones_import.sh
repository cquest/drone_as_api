wget -nc http://data.cquest.org/dgac/restrictions_drones/restrictions_drones_201811.json.gz
ogr2ogr -f postgresql PG:"dbname=$USER" -nln drones -nlt geometry /vsigzip/restrictions_drones_201811.json.gz
psql -c "
ALTER TABLE drones DROP fid;
ALTER TABLE drones ALTER limite type integer USING limite::integer;
"
