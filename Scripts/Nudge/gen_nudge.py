#! /usr/bin/env python
from datetime import datetime, timedelta
import logging
import os
import pathlib
import shutil
import tarfile
import tempfile
import unittest
import urllib.request

from pyschism import dates
from pyschism.mesh import Hgrid, Vgrid
from pyschism.forcing.hycom.hycom2schism import Nudge


logging.basicConfig(level=logging.INFO, force=True)


if __name__ == '__main__':

    hgrid=Hgrid.open('../../data/hgrid.gr3', crs='epsg:4326')
    vgrid='../../data/vgrid.in'
    outdir='./'
    start_date = datetime(2022, 4, 1)
    rnday=10

    nudge=Nudge()
    nudge.fetch_data(outdir, hgrid, vgrid, start_date, rnday)
