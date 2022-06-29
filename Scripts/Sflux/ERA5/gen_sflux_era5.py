from datetime import datetime
from time import time
import pathlib

from pyschism.forcing.nws.nws2.era5 import ERA5

from pyschism.mesh.hgrid import Hgrid

if __name__ == '__main__':

    startdate=datetime(2003, 9, 8)
    rnday=10

    hgrid=Hgrid.open('../../../data/hgrid.gr3',crs='EPSG:4326')
    bbox = hgrid.get_bbox('EPSG:4326', output_type='bbox')

    outdir = pathlib.Path('./')

    #output interval
    interval = 3

    t0=time()

    cache = './'

    er=ERA5(cache=cache)

    er.write(outdir=outdir, start_date=startdate, rnday=rnday, air=True, \
        rad=True, prc=True, bbox=bbox, output_interval=interval, overwrite=True)

    print(f'It took {(time()-t0)/60} minutes to generate {rnday} days')
