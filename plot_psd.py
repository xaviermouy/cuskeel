""""
This script goes though a folder of csv created by MANTA and convert  csv to nc files

"""

import pandas as pd
import xarray as xr
import os
import glob
import pathlib
#import pypam
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import dates
matplotlib.use('TkAgg')

in_dir = r'C:\Users\xavier.mouy\Documents\Projects\2025_Wellfleet\PBP_analysis_results\WellfleetHarbor_2023-07'
#target_freqband_hz = [1031.5731, 2058.2588]
target_freqband_hz = [1000, 2000]

## Load all data
dir_path = pathlib.Path(in_dir)#.joinpath(station)
nc_files = [f for f in dir_path.rglob("*.nc")]
ds = xr.open_mfdataset(nc_files, concat_dim = "time",combine = "nested", engine = 'netcdf4')

# LTSA
integration_time = '30min'
psd_resampled = ds.psd.resample(time=integration_time).mean()  # Resample to daily spectra
psd_resampled.plot(x='time', y='frequency')
plt.show()

# select only frequency band of interest
ds_cuskeel_band = ds.sel(frequency=slice(min(target_freqband_hz),max(target_freqband_hz))) # select only given year

# Cusk eel metrics
ds_cuskeel_metrics = ds_cuskeel_band.mean(dim='frequency')

# plot
#ds_cuskeel_metrics.psd.plot()
#plt.show()
#print('s')


## plot PSD
integration_time = '20min'
ds_cuskeel_metrics_resampled = ds_cuskeel_metrics.psd.resample(time=integration_time).mean()  # Resample to daily spectra
ds_cuskeel_metrics_resampled.plot()
plt.show()
print('s')
