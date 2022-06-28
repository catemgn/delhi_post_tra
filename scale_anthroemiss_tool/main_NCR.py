# load modules 
import xarray as xr
import numpy
import os
import pandas as pd
import json

# define functions

def modify_sec_emiss(ds,emi_list,share):

    ''' 
    Create function for modifying emissions for each subsector given emissions 
    file (ds, xarray), list of emissions species (emi_list, xlsx), 
    and scaling factors by subsector (share, xlsx).
    '''

    #create empty new dataset
    ds_t= xr.Dataset({})
    
    #loop along all species.
    for v,z in emi_list.items():
        
        # keep to zero emissions tha are zero.
        if z: # z=1 means is_zero is true.
            ds_t['E_'+v]=ds['E_'+v]
            ds_t['E_'+v].attrs=ds['E_'+v].attrs  # add attribute infos as in original wrfchemi. 
        else:    
            for sec, shr in share.items():
                # modify subsector emi (differnet masks if NCT or NCR).
                if sec.startswith('NCR'):
                    ds_t['E_'+v+'_'+sec]=ds['E_'+v+'_'+sec[4:]]*mn*shr  #NCR
                else:
                    ds_t['E_'+v+'_'+sec]=ds['E_'+v+'_'+sec]*m*shr   #NCT
                  
            # for each species add all emi together from all subsectors
            ds_t['E_'+v]=sum(ds_t['E_'+v +'_'+ s] for s in share.keys())
            ds_t['E_'+v].attrs=ds['E_'+v+'_'+'NCR_TOT'].attrs  # add attribute infos as in original wrfchemi.
    
    # create final summed emi data
    ds_t=ds_t[[('E_'+v) for v in emi_list.keys()]]
    
    # add XLAT,XLONG,Time
    ds_t['XLAT']=ds['XLAT']
    ds_t['XLONG']=ds['XLONG']
    ds_t['Times']=ds['Times']
    
    return ds_t



def fill_ncr_emiss(ds_e,ds_t):
    '''
    Fills wrfchem domain with EDGARv5 emissions where the domain is not 
    covered by the Delhi inventory. ds_e: edgar wrfchemi emission file. 
    ds_t: Delhi wrfhcemi emission file.
    '''
    ds=ds_t.copy()
    for v in ds_t.data_vars:
    # based on where teri inventory is zero, substitue with EDGARv5 values.
        if (v!='Times') & (v!='XLONG') & (v!='XLAT'):
            ds[v]=ds_t[v].where(ds_t[v]>0.0,ds_e[v])   

    return ds



# load masks

m=xr.open_dataset('./NCT_mask.nc').co
mn=xr.open_dataset('./NCR_mask.nc').co

#load emissions and scaling files.
with open('share_NCR.json', "r") as read_file:
     share= json.load(read_file)
# list of anthro emissions in WRF-Chem. NOTE: species starting with 'zero' 
#means they are zero in the anthro emiss mapping. 
# Thus they will be put as zero directly also in the final sum.'
with open('emi_list.json', "r") as read_file:
     emi_list= json.load(read_file)


# Get edgar5 emiss onto nested domain
e=xr.open_dataset('./wrfchemi_00z_d02')


input_dir='./emi_base/'
out_dir='./emi_modified/'



# modify share of emissions + fill background create for all wrfchemi files
for f in os.listdir(input_dir):
    if f.startswith('wrfchemi_'):
        print(f)
        t=xr.open_dataset(input_dir+f)
        
        #modify sectors emissions
        ncr=modify_sec_emiss(t,emi_list,share)
       
        #fill background with EDGAR 
        ncr=fill_ncr_emiss(e.mean('Time'),ncr)
        
        # save files
        ncr.chunk().to_netcdf(out_dir+f,format='NETCDF3_64BIT') 
