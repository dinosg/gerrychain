from ._version import get_versions
from .chain import MarkovChain
from .chain_xtended import MarkovChain_xtended
#from .chain_xtended_polish import MarkovChain_xtended_polish
from .graph import Graph
from .partition import GeographicPartition, Partition
from .updaters.election import Election

__version__ = get_versions()['version']
del get_versions
