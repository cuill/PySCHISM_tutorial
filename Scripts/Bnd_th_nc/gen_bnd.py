from datetime import datetime
import logging

from pyschism.mesh.hgrid import Hgrid
from pyschism.forcing.hycom.hycom2schism import OpenBoundaryInventory

logging.basicConfig(level=logging.INFO, force=True)

if __name__ == "__main__":
    hgrid=Hgrid.open('../../data/hgrid.gr3', crs='epsg:4326')
    print(hgrid.bbox)
    vgrid='../../data/vgrid.in'
    outdir='./'
    start_date=datetime(2022, 4, 1)
    rnday=10
    lats=[0, 27, 28, 32, 33, 90] 
    msl_shifts=[-0.25, -0.25, 0.0, 0.0, 0.56, 0.56]

    bnd=OpenBoundaryInventory(hgrid, vgrid)
    bnd.fetch_data(outdir, start_date, rnday, elev2D=True, TS=True, UV=True, adjust2D=True, lats=lats, msl_shifts=msl_shifts)
