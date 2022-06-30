from pyschism.mesh.hgrid import Hgrid

from pyschism.mesh.fgrid import DragCoefficient

if __name__ == '__main__':

    hgrid=Hgrid.open('../../../data/hgrid.gr3', crs='epsg:4326')

    # depth < -3, bfric=0.025, depth > -1, bfric = 0.0025, [-3, -1], linear with depth
    depth1=-1.0
    depth2=-3.0
    bfric_river=0.0025
    bfric_land=0.025

    fgrid=DragCoefficient.linear_with_depth(hgrid, depth1, depth2, bfric_river, bfric_land)

    #Modify by region
    regions=['GoME+0.001.reg', 'Lake_Charles_0.reg']
    values=[0.001, 0.0]
    flags=[1, 0] # 0: set, 1: add
    for reg, value, flag in zip(regions, values, flags):
        fgrid.modify_by_region(hgrid, f'./{reg}', value, depth1, flag)

    fgrid.write('drag.gr3', overwrite=True)
