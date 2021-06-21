"""
this Markov chain forces more compact districts - with smaller boundary length
and permit lower mean_median scores as long as those >= 0
"""

from .constraints import Validator
from gerrychain import updaters
from gerrychain.metrics import mean_median
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

class MarkovChain_xtended_polish:
    """
    THIS version requires the next state have shorter boundary length AND higher mean_median than current state...
    making better looking districts without compromising median - mean
    MarkovChain is an iterator that allows the user to iterate over the states
    of a Markov chain run.

    Example usage:

    .. code-block:: python

        chain = MarkovChain(proposal, constraints, accept, initial_state, total_steps)
        for state in chain:
            # Do whatever you want - print output, compute scores, ...

    """

    def __init__(self, proposal, constraints, accept, initial_state, total_steps, my_electionproxy, maxsplits):
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
        self.my_electionproxy = my_electionproxy
        self.maxsplits = maxsplits
        
    

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
                if self.accept(proposed_next_state) and self.fit == 1 and (total_splits(self.state) >= total_splits(proposed_next_state)) and \
                	(len(self.state["cut_edges"]) >=   len(proposed_next_state["cut_edges"]) ) \
                        and ((mean_median(self.state[self.my_electionproxy]) <= mean_median(proposed_next_state[self.my_electionproxy])) \
                             or (mean_median(proposed_next_state[self.my_electionproxy]) >= 0)):
                    self.state = proposed_next_state
                    if total_splits(self.state) <= self.maxsplits:
                        self.good=1
                      #  self.fit = 0  #reset so don't do any more fits for the next 100 after this
                        self.lastgoodcount = self.counter
                        self.counter += 1
                    else:
                        self.good=0
                        
                    
                elif self.accept(proposed_next_state) and self.fit == 0:  #"dont bother trying to reduce county splits but scramble state"
                    self.state = proposed_next_state
                    self.good=0
                    
                    
                elif self.accept(proposed_next_state) and self.fit ==1 and total_splits(proposed_next_state) <= self.maxsplits and \
                (len(self.state["cut_edges"]) >=   len(proposed_next_state["cut_edges"])) \
                    and ((mean_median(self.state[self.my_electionproxy]) <= mean_median(proposed_next_state[self.my_electionproxy])) \
                         or (mean_median(proposed_next_state[self.my_electionproxy]) >= 0)):
                    self.good=1
                    self.state = proposed_next_state
                    self.counter += 1
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
