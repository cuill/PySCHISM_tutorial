from datetime import datetime, timedelta
from time import time
import multiprocessing as mp
import logging

import numpy as np
import pandas as pd

from pyschism.mesh.hgrid import Hgrid
from pyschism.forcing.nws.nws2.gfs2 import GFS
from pyschism.dates import nearest_cycle

logging.basicConfig(
    format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
    force=True,
)
logging.captureWarnings(True)

log_level = logging.DEBUG
logging.getLogger('pyschism').setLevel(log_level)

if __name__ == "__main__":
    t0 = time()

    startdate = datetime(2022, 3, 31)
    hgrid = Hgrid.open('../../../data/hgrid.gr3', crs='epsg:4326')
    pscr = '/sciclone/pscr/lcui01/GFS/'
    rnday = 11
    record = 1
    gfs = GFS(start_date=startdate, rnday=rnday, pscr=pscr, record=record, bbox=hgrid.bbox)

    #gfs.gen_sflux(startdate, record=record)
    print(f'It took {(time()-t0)/60} mins to process {rnday} days, {record*24} records/day')
