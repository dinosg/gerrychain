# gerrychain
modifications &amp; adds to gerrychain software, as in https://gerrychain.readthedocs.io/en/latest/user/install.html

runningachain_plain.py duplicates what's available in the gerrychain archive, with input variables read in from a file (stored in input_templates) and the type of Markov chain proposal

runningachain_50.pc adds a normalizing feature to treat the statewide election used as a proxy for votes by district, as a 50-50% partisan split. Thus the results by district, if they differ by a 50-50 allocation on average, are the result of gerrymandering and not the strength of the statewide candidate used as a voter proxy by district

chain_parallelx.py uses the multiprocessing module to implement a parallel pool. I achieved an x 36 speed increase on my server (40 core). It also uses condense_datastruct.py to unwrap the datastructure created by a parallel markov chain computation, and only select one out of every nn (default 100) data rows to avoid tons of correlated, duplicate-ish data

chain_parallel_50.py uses multiprocessing and normalizes the statewide election proxy to 50-50%. 

strcmp_matlab.py does some string recognition and indexing what I'm used to doing (as in Matlab)

Districts are indexed in the panda DataFrame objects to the actual congressional (or whatever) district names, in a format friendly to congressmen and politicians, by get_districtlabels.py


any file with 'composite' or 'comp' in the filename adds ALL elections available to it in the dataset and calculates metrics covering ALL of them (by numeric mean) as to avoid biasing a result by a single idiosyncratic election

files with 'ppartonly' in name do NOT compute Markov chains at all but instead generate random partitions each and every time to get unbiased samples. Slow but necessary for cases when  Markov chain fails (as they often do for State House districts)

splice_assignment_fn.py  'splices in' a new district assignment from a csv/ text files and merges it to an existing geodataframe with state VTD shapes and election data, defines my_apportionment to be something new (reflecting what's in the file). Extremely useful for assessing test plans, or constructing new
district mappings from intermediate stored results

conditional_dump.py tests a partition state against some condition - if it meets it, dumps out the VTD assignments to a text file. Uses routines in district_list.py for output
****
county splits & gerrychain modifications:

files with 'county' in name have maximum # county splits as a constraint. These files require modifications to gerrychain class - see 'runningachain_xtended' for simple case.

chain_xtended.py needs to be included in sourcecode gerrychain directory
_init_.py and county_splits.py need to be included in sourcecode gerrychain/updaters directory

county_splits.py is modified from original - MUST go in gerrychain/updaters folder  for county split computations to work 
total_splits.py computes the # of county splits - looking for the specific text tag in a shapefile that indicates county name (these differ among states)
______

directed search algorithms:
these files don't use gerrychain as a random ensemble for statistical analysis but instead use it for random evolution with particular constraints to identify plans with desired characteristics: fewer county splits, more or less democratic seats, better compactness. They call *modified* gerrychain markov chain classes.

fewer county splits:    scripts with _shrink_ 
                        calls MarkovChain_xtended in chain_xtendedpy
                        
more democratic fractional seats: scripts with _fracwinsgt.py. accepts plans that increase the democratic wins of fractional seats
                                  calls MarkovChain_xtendedfracwinsgt  in chain_xtendedfracwinsgt.py
                                  
fewer democratic fractional seats: scripts with _ltfracwins_. accepts plans that decrease the dem wins of fractional seats
                                    calls MarkovChain_xtended_ltpolish_fracs  in chain_xtended_polish_ltfracs.py
                                    
higher median-mean:                scripts with _mmgt - accepts plans that increase mean_median() metric function
                                   calls MarkovChain_xtendedmmgt  in chain_xtendedmmgt.py
                                   
better compactness:                scripts with smooth,  - accepts plans that *reduce* cut_edges
                                   calls MarkovChain_xtended_polish_fracs in chain_xtended_polish_fracs.py, if preserving dem seat share (to an extent)
                                   or,
                                   MarkovChain_xtended_polish_fracs_repub in chain_xtended_polish_fracs_repub.py, if preserving republican seat share
______
input_templates:
contains template files - eg. (state)_race_proxyelection.py  eg. MI_SENDIST_PRES16.py (michigan, state senate districting using 16 pres election as proxy) setting input variables, eg filenames, tagnames, the name of the district type to analyze etc. all in 1 place to be read into script running gerrychain... avoiding all those confusing parameters that need to be set differently depending on the run you're doing. 

_____
corrected datafiles:

TX_vtds_x.zip   contains *fixed* shapefiles for Texas - original data archive from https://github.com/mggg-states  wasn't readable due to a point boundary in the North Texas panhandle... this shapefile was buffered and healed

WI_ltsb_corrected_final.json contains *fixed* shapefiles for Wisconsin, with no disconnected islands

MI_precincts.json contains *fixed* shapefiles for Michigan, no islands, UP and LP connected (!)

PA2020_2019pop.zip is the PA election data file using 2020 census precinct shapes, 2019 American Community Survey population estimates. Includes 2018 election data


WI2020_censusvtds_overlap_pop19.zip contains updated WI shapefiles & data, using 2020 census vtds, 2019 population estimates

OH_2020_censusvtds_2019pop.zip contains updated OH shapefiles & data, using 2020 census vtds, 2019 population estimates

