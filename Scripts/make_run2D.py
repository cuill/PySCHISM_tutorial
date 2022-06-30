from time import time
import os
from datetime import datetime, timedelta
import logging
import pathlib
import f90nml
import shutil

from pyschism.mesh import Hgrid, Gr3
from pyschism.mesh.vgrid import Vgrid
from pyschism.mesh.gridgr3 import ElevIc, Windrot, Shapiro
from pyschism.mesh.fgrid import ManningsN
from pyschism.forcing.bctides import Bctides, iettype, ifltype
from pyschism.forcing.source_sink.nwm import NationalWaterModel, NWMElementPairings
from pyschism.forcing.nws import ERA5
from pyschism.forcing.hycom.hycom2schism import OpenBoundaryInventory

def update_param(startdate, rnday, nml, outdir):
    nml['CORE']['rnday'] = rnday
    nml['OPT']['start_year'] = startdate.year
    nml['OPT']['start_month'] = startdate.month
    nml['OPT']['start_day'] = startdate.day
    nml['OPT']['start_hour'] = startdate.hour

    nml.write(outdir / 'param.nml', force=True)

if __name__ == "__main__":

    #setup logging
    logging.basicConfig(
        format = "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
        force=True,
    )
    logging.getLogger("pyschism").setLevel(logging.DEBUG)

    #input information
    run_name = 'RUN'
    run_dir = pathlib.Path(run_name)
    run_dir.mkdir(exist_ok = True, parents = True)

    startdate = datetime(2022, 4, 4)
    rnday = 10

    ##output directory 
    #outputs = pathlib.Path(f"/sciclone/scr10/lcui01/ICOGS2D/outputs_{run_name}")
    #outputs.mkdir(exist_ok = True, parents = True)
    #dst = pathlib.Path(f"./{run_dir}/outputs")
    #os.symlink(outputs, dst)

    #update param.nml
    nml = f90nml.read('./param_template.nml')
    update_param(startdate, rnday, nml, run_dir)

    #hgrid
    hgrid = Hgrid.open("./hgrid.gr3", crs="epsg:4326")
    bbox = hgrid.get_bbox('EPSG:4326', output_type='bbox')

    #link hgrid to run_dir
    src = '/sciclone/schism10/lcui01/schism20/ICOGS/ICOGS2D/RUN_SM/hgrid.gr3'
    os.symlink(src, run_dir / 'hgrid.gr3')

    #des = './hgrid.ll'
    os.symlink(src, run_dir / 'hgrid.ll')

    #link station file
    src = '/sciclone/schism10/lcui01/schism20/ICOGS/ICOGS2D/RUN_SM/station.in'
    os.symlink(src, run_dir / 'station.in')

    #vgrid (2D)
    h_s = 1.e6
    ztot = [-1.e6]
    h_c = 100.
    theta_b = 0.
    theta_f = 1.e-4
    sigma = [-1., 0.]
    vgrid = Vgrid.v2d(h_s, ztot, h_c=h_c, theta_b=theta_b, theta_f=theta_f, sigma=sigma)
    vgrid.write(run_dir / 'vgrid.in', overwrite=True)

    #manning.gr3
    min_value = 0.02
    max_value = 0.05
    min_depth = -1.0
    max_depth = -3.0
    fgrid=ManningsN.linear_with_depth(hgrid, min_value, max_value, min_depth, max_depth)
    #regions for certain values
    regions=('GoME_1.reg','GoME_2.reg','Berwick.reg','BulkTerminal.reg','Pilottown.reg')
    rvalues=(0.2, 0.2, 0.005, 0.005, 0.005)
    for reg,rval in zip(regions, rvalues):
        fgrid.modify_by_region(hgrid, reg, rval, min_depth, flag=0)
    fgrid.write(run_dir / 'manning.gr3', overwrite=True)

    #shapiro.gr3 (ishapiro = -1)
    shapiro_max=0.5
    threshold_slope=0.5
    depths=[-99999, 20, 50]
    shapiro_vals1=[0.2, 0.2, 0.05]
    regions = ['coastal_0.2.cpp.reg', 'coastal_0.5_1.cpp.reg', 'coastal_0.5_2.cpp.reg']
    shapiro_vals2=[0.2, 0.5, 0.5]
    i_set_add_s=[0, 0, 0]
    shapiro=Shapiro.slope_filter(hgrid, shapiro_vals1, depths, shapiro_max, threshold_slope, \
            regions, shapiro_vals2, i_set_add_s, lonc = -77.07, latc = 24.0)
    shapiro.write(run_dir / 'shapiro.gr3', overwrite=True)

    #elev.ic
    hgrid_orig = Gr3.open('./hgrid.gr3', crs='epsg:4326')
    #define region
    region = 'include.reg'
    elevic = ElevIc.modify_by_region(hgrid_orig, region, lonc = -77.07, latc = 24.0)
    elevic.write(run_dir / 'elev.ic', overwrite=True)

    #windrot
    windrot = Windrot.default(hgrid)
    windrot.write(run_dir / "windrot_geo2proj.gr3", overwrite=True)

    #Bctides
    iet3 = iettype.Iettype3(constituents='major', database='tpxo')
    iet4 = iettype.Iettype4()
    iet5 = iettype.Iettype5(iettype3=iet3, iettype4=iet4)
    ifl3 = ifltype.Ifltype3(constituents='major', database='tpxo')
    bctides=Bctides(hgrid, iettype=iet5, ifltype=ifl3)
    bctides.write(run_dir, startdate, rnday, bctides=True, elev2D=False, uv3D=False, tem3D=False, overwrite=True)

    #NWM
    sources_pairings = run_dir / 'sources.json'
    sinks_pairings = run_dir / 'sinks.json'
    cache = pathlib.Path(f'./{startdate.strftime("%Y%m%d")}')
    cache.mkdir(exist_ok=True, parents=True)

    if all([sources_pairings.is_file(), sinks_pairings.is_file()]) is False:
        pairings = NWMElementPairings(hgrid)
        sources_pairings.parent.mkdir(exist_ok=True, parents=True)
        pairings.save_json(sources=sources_pairings, sinks=sinks_pairings)
    else:
        pairings = NWMElementPairings.load_json(
            hgrid,
            sources_pairings,
            sinks_pairings)

    nwm=NationalWaterModel(pairings=pairings, cache=cache)
    nwm.write(run_dir, hgrid, startdate, rnday, overwrite=True)
    
    #elev2D
    lats=[0, 28, 32, 90]
    msl_shifts=[0.7, 0.7, 0.6, 0.6]
    bnd=OpenBoundaryInventory(hgrid)
    bnd.fetch_data(run_dir, startdate, rnday, elev2D=True, TS=False, UV=False, adjust2D=True, lats=lats, msl_shifts=msl_shifts)

    #sflux
    er=ERA5()
    outdir = (run_dir / "sflux").mkdir(exist_ok=True, parents=True)

    er.write(outdir= run_dir / "sflux", start_date=startdate, rnday=rnday, air=True, rad=False, prc=False, bbox=bbox, overwrite=True)

