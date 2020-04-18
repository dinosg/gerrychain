# gerrychain
modifications &amp; adds to gerrychain software, as in https://gerrychain.readthedocs.io/en/latest/user/install.html

runningachain_plain.py duplicates what's available in the gerrychain archive, with some options to specify input variables and the type of Markov chain proposal

runningachain_50.pc adds a normalizing feature to treat the statewide election used as a proxy for votes by district, as a 50-50% partisan split. Thus the results by district, if they differ by a 50-50 allocation on average, are the result of gerrymandering and not the strength of the statewide candidate used as a voter proxy by district

chain_parallel.py uses the multiprocessing module to implement a parallel pool. I achieved an x 36 speed increase on my server (40 core). It also uses condense_datastruct.py to unwind the datastructure created by a parallel markov chain computation

chain_parallel_50.py uses multiprocessing and normalizes the statewide election proxy to 50-50%.

strcmp_matlab.py does some string recognition and indexing what I'm used to doing (as in Matlab)

Districts are indexed in the panda DataFrame objects to the actual congressional (or whatever) district names, in a format friendly to congressmen and politicians, by get_districtlabels.py


