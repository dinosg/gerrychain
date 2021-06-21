from .constraints import Validator
from gerrychain import updaters
from gerrychain.metrics import mean_median
from calc_fracwins_comp import calc_fracwins_comp
def total_splits(partition):
        
    #county_field  = 'COUNTYFP10'
    #county_field = "COUNTY"
    fieldlist = partition.graph.nodes[0].keys()   #get LIST OF FIELDS
    
    if 'COUNTYFP10' in fieldlist:
        county_field = 'COUNTYFP10'
    elif 'CTYNAME' in fieldlist:
        county_field = 'CTYNAME'
    
    elif 'COUNTYFIPS' in fieldlist:
        county_field = 'COUNTYFIPS'
    
    elif 'COUNTYFP' in fieldlist:
        county_field = 'COUNTYFP'
    elif 'cnty_nm' in fieldlist:
        county_field = 'cnty_nm'
    elif 'county_nam' in fieldlist:
        county_field = 'county_nam'
    elif 'FIPS2' in fieldlist:
        county_field = 'FIPS2'
    
    elif 'County' in fieldlist:
        county_field = 'County'
    elif 'FIPS' in fieldlist:
        county_field = 'FIPS'
    elif 'CNTY_NAME' in fieldlist:
        county_field = 'CNTY_NAME'
    elif 'COUNTY' in fieldlist:
        county_field = 'COUNTY'
    else:
        print("no county ID info in shapefile\n")
        return 10
    
    gg = updaters.county_splits(partition, county_field)
    gg_res = gg(partition)
    splitcount=0
    for x in gg_res:
        splitcount+= len(gg_res[x].contains) -1 #subtract 1 b/c there's 1 county listed if there are no splits
        
    return splitcount



class MarkovChain_xtendedfracwinsgt:
    """
    MarkovChain is an iterator that allows the user to iterate over the states
    of a Markov chain run.

    Example usage:

    .. code-block:: python

        chain = MarkovChain(proposal, constraints, accept, initial_state, total_steps)
        for state in chain:
            # Do whatever you want - print output, compute scores, ...

    this version requires mean_median
    """
    
    def __init__(self, proposal, constraints, accept, initial_state, total_steps, election_composite, maxsplits, win_volatility):
        """
        :param proposal: Function proposing the next state from the current state.
        :param constraints: A function with signature ``Partition -> bool`` determining whether
            the proposed next state is valid (passes all binary constraints). Usually
            this is a :class:`~gerrychain.constraints.Validator` class instance.
        :param accept: Function accepting or rejecting the proposed state. In the most basic
            use case, this always returns ``True``. But if the user wanted to use a
            Metropolis-Hastings acceptance rule, this is where you would implement it.
        :param initial_state: Initial :class:`gerrychain.partition.Partition` class.
        :param total_steps: Number of steps to run.
        
        :param maxsplits - max # of county splits
        : param election_composite - list of elections to assess fractional seat wins for
        : param win_volatility - volatility of election results eg. John Nagle ref, 5% for PA so can assess
          fractional seat win probability
        : seat_min - for polish step, don't increase compactness if number of seats falls below this  
        """
        if callable(constraints):
            is_valid = constraints
        else:
            is_valid = Validator(constraints)

        if not is_valid(initial_state):
            failed = [
                constraint
                for constraint in is_valid.constraints
                if not constraint(initial_state)
            ]
            message = (
                "The given initial_state is not valid according is_valid. "
                "The failed constraints were: " + ",".join([f.__name__ for f in failed])
            )
            self.good = 0
            raise ValueError(message)

        self.proposal = proposal
        self.is_valid = is_valid
        self.accept = accept
        self.good = 1
        self.total_steps = total_steps
        self.initial_state = initial_state
        self.state = initial_state
        self.lastgoodcount = 0
        self.maxsplits = maxsplits
        self.election_composite = election_composite
        self.win_volatility = win_volatility
        
    

    def __iter__(self):
        self.counter = 0
        self.state = self.initial_state
        self.good=1
        self.fit = 1
        return self

    def __next__(self):
        
        if self.counter == 0:
            self.counter += 1
            self.good=1
        
            return self
            
        
        while self.counter < self.total_steps:
        
            proposed_next_state = self.proposal(self.state)
            # Erase the parent of the parent, to avoid memory leak
            self.state.parent = None
            if self.counter - self.lastgoodcount > 100:  #%fit & get new data that attemps to lower county splits.
                self.fit = 1
            if self.is_valid(proposed_next_state):
                if self.accept(proposed_next_state) and self.fit == 1 and (total_splits(self.state) >= total_splits(proposed_next_state)) \
                    and (calc_fracwins_comp(self.state, self.election_composite, self.win_volatility) <= \
                         calc_fracwins_comp(proposed_next_state,self.election_composite, self.win_volatility )):
                        
                    if calc_fracwins_comp(self.state,self.election_composite, self.win_volatility  ) <  \
                        calc_fracwins_comp(proposed_next_state, self.election_composite, self.win_volatility):
                        
                        self.good = -1
                    else:
                        self.good = 0
                    self.state = proposed_next_state
                       
                        
                elif self.accept(proposed_next_state) and self.fit == 0:  #"dont bother trying to reduce county splits but scramble state"
                    self.state = proposed_next_state
                    self.good=0
                    
                    
                    #so ANYTIME splits <= maxsplits self.good =1 even if mm of proposed state satisfied >= criteria
                        #that is, self.good = 1 AND self.good = -1 ARE good cases to check and dump output to get progress on mean_median
                        
                elif self.accept(proposed_next_state) and self.fit ==1 and total_splits(proposed_next_state) <= self.maxsplits \
                    and (calc_fracwins_comp(self.state, self.election_composite, self.win_volatility) <=  \
                         calc_fracwins_comp(proposed_next_state,self.election_composite, self.win_volatility )):
                        if (calc_fracwins_comp(self.state, self.election_composite, self.win_volatility)  < \
                            calc_fracwins_comp(proposed_next_state,self.election_composite, self.win_volatility )):
                            self.good = -1
                        else:
                            self.good = 0
                        self.state = proposed_next_state
                    
                    #self.good=1
                       
                else:
                    self.good=0
                
                
                return self
            else:
                self.good=0
        raise StopIteration

    def __len__(self):
        return self.total_steps

    def __repr__(self):
        return "<MarkovChain [{} steps]>".format(len(self))

    def with_progress_bar(self):
        from tqdm.auto import tqdm

        return tqdm(self)
