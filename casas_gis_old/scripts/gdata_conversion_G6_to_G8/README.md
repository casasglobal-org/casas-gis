## Objectives

The large GRASS GIS 6.4 database that CASAS has built so far, including
geospatial information layers used for mapping and analysis by the
extant CASAS geospatial software, has been migrated to GRASS GIS 8
using a set of scripts as described below. The conversion scripts have
been executed on the 45 GRASS GIS 6 formatted CASAS mapsets.

## Vector data conversion

The upgrade steps are (in a loop):

- all maps: rebuilding of the vector topology from GRASS GIS 6 (a few
  GRASS GIS 5 vector maps have been discovered as well) to GRASS GIS 8
- all DBF-mapsets: attribute transfer from DBF to SQLite; susequent
  deletion of `dbf/` subdirectory in respective mapset if file is empty

It took approx 40 min on an Intel Core i7 system to upgrade the GRASS
GIS 6 vector data to GRASS GIS 8 including the rebuilding of vector
topology and attribute transfer from DBF to SQLite.

Observations:

- a few isolated dbf files remained in a few mapsets which were unconnected
  to vector maps
- a few leftover files have been removed (apparently incompletely deleted
  vector maps with only helper files left over; documented in the preparation script).
- In the (few) mapsets which already used SQLite only the topology
  has been rebuilt:
  - Here the dbf files remained since no decision could be taken by the
    contractor if the files are still relevant or not. They are easy to
    spot by a file extension search.

A conversion log file is generated for inspection.

## Raster data conversion

The upgrade steps were (in a loop):

- set computational region to actual raster map
- regenerate the map statistics

Observations:

- one raster map is using `r.external` (path: `/Users/luigi/olive_distribution_pnas.tif`) .
  This map was not yet included in the Zenodo.org database. It could be
  included and placed in the same mapset.

It takes approx 15 min on an Intel Core i7 system to update the GRASS GIS 6
raster statistics to GRASS GIS 8.

A conversion log file is generated for inspection.

## Developed scripts

The scripts have been developed in a modular way.

An approach to directly convert from GRASS GIS 6 to GRASS GIS 8 format
has been identified.

The subsequent scripts expect a GRASS GIS 8.4+ installation to be
available on the machine.

1\) Preprocessing script:

- `process_grass6data_casas.sh`:
  - unpacks GRASS GIS 6 database (ZIP format)
  - informs user about next scripts to be run

2\) Vector data upgrade script:

- `vector_convert_all_mapsets_G6_G8.sh`:
  - loops over all mapsets and runs:
    - `v.db.dbf2sqlite.all.sh`:
      - performs vector topology upgrade and migration from DBF
        base attributes to SQLite

Requirement:

- `v.db.reconnect.all.py.diff`:
  - note: a modification is needed in `v.db.reconnect.all` (GRASS
    GIS 8) to turn fatal error existing on incomplete or already
    SQLite-connected vector maps into a warning. Like this the
    loop-oriented conversion continues.
  - To be applied in the GRASS GIS source code with:
    - `patch -p1 < v.db.reconnect.all.py.diff`

3\) Raster data upgrade script:

- `raster_convert_all_mapsets_G6_G8.sh`:
  - loops over all mapsets and runs:
    - `rsupport.stats.all.sh`:
      - performs update of raster map statistics (including
        creation of new internal files as per GRASS GIS 8).
