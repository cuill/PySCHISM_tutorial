from pyschism.mesh.hgrid import Hgrid
from pyschism.mesh.fgrid import ManningsN

if __name__ == '__main__':

    hgrid = Hgrid.open('../../../data/hgrid.gr3', crs='epsg:4326')

    #mannings
    min_value = 0.02
    max_value = 0.05
    min_depth = -1.0
    max_depth = -3.0
    fgrid=ManningsN.linear_with_depth(hgrid, min_value, max_value, min_depth, max_depth)
  
    #regions for certain values
    regions=('GoME_1.reg','GoME_2.reg','Berwick.reg','BulkTerminal.reg','Pilottown.reg')
    rvalues=(0.2,0.2,0.005,0.005,0.005)

    for reg,rval in zip(regions, rvalues):
        fgrid.modify_by_region(hgrid, reg, rval, min_depth, flag=0)

    fgrid.write('manning.gr3', overwrite=True)

