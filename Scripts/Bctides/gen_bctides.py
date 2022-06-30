from datetime import datetime, timedelta
import logging
#import pathlib
#import f90nml

from pyschism.mesh import Hgrid
from pyschism.forcing.bctides import Bctides, iettype, ifltype, isatype, itetype

if __name__ == "__main__":

    #setup logging
    logging.basicConfig(
        format = "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
        force=True,
    )
    logging.getLogger("pyschism").setLevel(logging.DEBUG)

    startdate = datetime(2022, 4, 4)
    print(startdate)
    rnday = 10
    hgrid = Hgrid.open("../../data/hgrid.gr3", crs="epsg:4326")

    #Bctides
    iet3 = iettype.Iettype3(constituents='major', database='tpxo')
    iet4 = iettype.Iettype4()
    iet5 = iettype.Iettype5(iettype3=iet3, iettype4=iet4)
    ifl3 = ifltype.Ifltype3(constituents='major', database='tpxo')
    ifl4 = ifltype.Ifltype4()
    ifl5 = ifltype.Ifltype5(ifltype3=ifl3, ifltype4=ifl4)
    isa3 = isatype.Isatype4()
    ite3 = itetype.Itetype4()
    bctides=Bctides(hgrid, iettype=iet5, ifltype=ifl5, isatype=isa3, itetype=ite3)
    bctides.write('./', startdate, rnday, bctides=True, elev2D=False, uv3D=False, tem3D=False, sal3D=False, overwrite=True)

