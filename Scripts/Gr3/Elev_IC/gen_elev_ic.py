from pyschism.mesh.base import Gr3
from pyschism.mesh.hgrid import Hgrid
from pyschism.mesh.gridgr3 import ElevIc

if __name__ == '__main__':

    hgrid = Gr3.open('../../../data/hgrid.gr3', crs='epsg:4326') 

    #define region
    region = 'include.reg'

    elevic = ElevIc.modify_by_region(hgrid, region, lonc = -77.07, latc = 24.0)
    elevic.write('elev.ic', overwrite=True)
