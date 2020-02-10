from packs.running.initial_mesh_properties import initial_mesh
from packs.pressure_solver.fine_scale_tpfa import FineScaleTpfaPressureSolver
from packs.directories import data_loaded
from packs.adm.adm_method import AdmMethod
from packs.multiscale.ms_utils.matrices_for_correction import MatricesForCorrection as mfc
from packs.multiscale.multilevel.multilevel_operators import MultilevelOperators
import numpy as np

load = data_loaded['load_data']
convert = data_loaded['convert_english_to_SI']
n = data_loaded['n_test']
load_operators = data_loaded['load_operators']
get_correction_term = data_loaded['get_correction_term']

M, elements_lv0, data_impress, wells = initial_mesh(load=load, convert=convert)
adm_method = AdmMethod(wells['all_wells'], 2, M, data_impress, elements_lv0)
adm_method.so_nv1 = True

adm_method.restart_levels()
adm_method.set_level_wells()
adm_method.set_adm_mesh()

tpfa_solver = FineScaleTpfaPressureSolver(data_impress, elements_lv0, wells)
T, b = tpfa_solver.run()

q_grav = data_impress['flux_grav_volumes'].copy()
total_source_term = b.copy()
total_source_term[data_impress['LEVEL']==0] = np.ones(len(total_source_term[data_impress['LEVEL']==0]))
q_grav[data_impress['LEVEL']==0] = np.zeros(len(q_grav[data_impress['LEVEL']==0]))

###################
## teste
rr = total_source_term==0
total_source_term[rr] = np.ones(len(total_source_term[rr]))
###################

# B_matrix_0 = mfc.get_B_matrix(total_source_term, q_grav)
#
# gid0 = data_impress['GID_0']
# volumes_without_grav = gid0[data_impress['VOLUMES_WITH_GRAV_1']==False]
#
# Eps_matrix_0 = mfc.get_Eps_matrix(gid0, volumes_without_grav)

mlo = MultilevelOperators(1, data_impress, M.multilevel_data, load=load_operators, get_correction_term=get_correction_term)
mlo.run(tpfa_solver['Tini'], b, q_grav)


import pdb; pdb.set_trace()
import pdb; pdb.set_trace()