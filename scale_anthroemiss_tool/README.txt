Date: 10/09/2021
Author: Caterina Mogno c.mogno@d.ac.uk

SCALE ANTHRO EMISSIONS SUBSECTOR TOOL WRF-Chem for DELHI

This python program scale emissions  of individual anthropogenic subsectors 
with user defined values over Delhi NCT and Delhi NCR (w\ NCT). 

INPUTS
- wrfchemi* files from anthro_emiss with explicit subsectors.Files: wrfchemi* in the emi_base/ folder.
- NCT and NCR masks: boolean masks for selecting NCT or NCR adiminstrative areas. Files: NCT_mask.nc, NCR_mask.nc.
- list of anthro emissions species in WRF-Chem. Files: emi_list.json.
- list of subsectors and their emissions  scale (1= identical to original emissions, 2=double, 0.5 = half etc). Files: share.json.
- wrfchemi file with EDGAR emissions over domain (for backgeound filling).Files: wrfchemi_00z_d02.

OUTPUTS
- wrfchemi* files with cutomised scaled anthropogenic emissions by subsector ready to be used for ./wrf.exe. 
Files: wrfchemi in the emi_modified/ folder.



FOR RUNNING:
1) modify share.json with desired share.
2) from command line: python3 main.py


NOTES:
- emi_list.json: this the list of chemical species in the emis_map of preprocessing tool for MOZART-MOSAIC anthro_emiss. 
1 or 0 values  indicates if the emissions from that species are initialised to zero 
emissions  in emis_map. (this will be useful when modify the share of emissions to directly initialise these species to zero).


