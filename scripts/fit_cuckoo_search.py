import numpy as np
import src.optimization.objective_functions as objf

from pathlib import Path
from src.UHECRs_sim_f import A_Z
from one_dimensional_propagation import run as run1D
from complete_propagation_Dolag_JF12 import run as run3D
from src.optimization.cuckoo_search import cuckoo_search
from src.utils.file_utils import check_dir, del_by_extension

numOfParams = len(A_Z)+2
##############################################################################################################
#                                   PROPAGATION SIMULATION VARIABLES
##############################################################################################################
    
root = '/home/caratheodory/development/astro_multimessenger_GAE/'
sourcesFile = Path(root).joinpath('data/EG_1D_sources.txt')
outDir = Path('./test_1D/')
numThousands = 1
noInteractions = True
parts = 1
check_dir(outDir)
obj_func = lambda r: objf.chi2_obj_func(sample=r,
                                        runPropFunc=run1D,
                                        srcPath=sourcesFile,
                                        outDir=outDir,
                                        num=numThousands,
                                        noInteractions=noInteractions,
                                        barProgress=False,
                                        parts=parts)

##############################################################################################################
#                                   CUCKOO SEARCH VARIABLES
##############################################################################################################
nHosts = 10
pa = 0.2
ranges = np.repeat(a=[[0,1]],
                   repeats=numOfParams,
                   axis=0)
maxIter = 20
checkpointDir = outDir.joinpath('checkpoints')
check_dir(checkpointDir)
bfResult = cuckoo_search(f=obj_func,
                         nHosts=nHosts,
                         pa=pa,
                         ranges=ranges,
                         maxIter=maxIter,
                         checkpointDir=checkpointDir,
                         loadCheckpoint=checkpointDir.joinpath('generation_20.checkpoint'),
                         alpha=1.25,
                         beta=0)

header = (27*' ').join(objf.orderedNuclei+['Rcut','alpha','chi2'])
np.savetxt(fname=outDir.joinpath('best_fit_parameters.txt'),
           X=bfResult,
           header=header,
           delimiter='    ')

del_by_extension(parentDir=Path(''), exts=('.pyc',), recursive=True)
