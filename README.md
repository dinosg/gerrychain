# gerrychain
modifications &amp; adds to gerrychain software, as in https://gerrychain.readthedocs.io/en/latest/user/install.html

runningachain_plain.py duplicates what's available in the gerrychain archive, with input variables read in from a file (stored in input_templates) and the type of Markov chain proposal

runningachain_50.pc adds a normalizing feature to treat the statewide election used as a proxy for votes by district, as a 50-50% partisan split. Thus the results by district, if they differ by a 50-50 allocation on average, are the result of gerrymandering and not the strength of the statewide candidate used as a voter proxy by district

chain_parallelx.py uses the multiprocessing module to implement a parallel pool. I achieved an x 36 speed increase on my server (40 core). It also uses condense_datastruct.py to unwrap the datastructure created by a parallel markov chain computation, and only select one out of every nn (default 100) data rows to avoid tons of correlated, duplicate-ish data

chain_parallel_50.py uses multiprocessing and normalizes the statewide election proxy to 50-50%. 

strcmp_matlab.py does some string recognition and indexing what I'm used to doing (as in Matlab)

Districts are indexed in the panda DataFrame objects to the actual congressional (or whatever) district names, in a format friendly to congressmen and politicians, by get_districtlabels.py

Certain simulation runs have problems running Markov chains - either because even after many chain steps, Markov states remain correlated, or the configurations become hung up (or both). Pennsylvania state House districts are one such case so instead of performing a Markov simulation, random districts are created for *each* successive state using recursive_tree_part from gerrychain. Timeout problems are avoiding using stopit (install using pip)


any file with 'composite' or 'comp' in the filename adds ALL elections available to it in the dataset and calculates metrics covering ALL of them (by numeric mean) as to avoid biasing a result by a single idiosyncratic election

files with 'ppartonly' in name do NOT compute Markov chains at all but instead generate random partitions each and every time to get unbiased samples. Slow but necessary for cases when  Markov chain fails (as they often do for State House districts)

splice_assignment_fn.py  'splices in' a new district assignment from a csv/ text files and merges it to an existing geodataframe with state VTD shapes and election data, defines my_apportionment to be something new (reflecting what's in the file). Extremely useful for assessing test plans, or constructing new
district mappings from intermediate stored results
****
county splits & gerrychain modifications:

files with 'county' in name have maximum # county splits as a constraint. These files require modifications to gerrychain class - see 'runningachain_xtended' for simple case.

chain_xtended.py needs to be included in sourcecode gerrychain directory
_init_.py and county_splits.py need to be included in sourcecode gerrychain/updaters directory

county_splits.py is modified from original - MUST go in gerrychain/updaters folder  for multithreaded computing to work 
______

input_templates:
contains template files - eg. (state)_race_proxyelection.py  eg. MI_SENDIST_PRES16.py (michigan, state senate districting using 16 pres election as proxy) setting input variables, eg filenames, tagnames, the name of the district type to analyze etc. all in 1 place to be read into script running gerrychain... avoiding all those confusing parameters that need to be set differently depending on the run you're doing. 

_____
corrected datafiles:

TX_vtds_x.zip   contains *fixed* shapefiles for Texas - original data archive from https://github.com/mggg-states  wasn't readable due to a point boundary in the North Texas panhandle... this shapefile was buffered and healed

WI_ltsb_corrected_final.json contains *fixed* shapefiles for Wisconsin, with no disconnected islands

MI_precincts.json contains *fixed* shapefiles for Michigan, no islands, UP and LP connected (!)



