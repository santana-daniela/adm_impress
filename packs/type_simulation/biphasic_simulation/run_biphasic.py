from ...simulations.init_simulation import rodar
from .biphasic_tpfa import biphasicTpfa
from .biphasic_tpfa import direc
import os


load = np.load(direc.name_load)[0]
verif = True
M = rodar.M
b1 = biphasicTpfa(M, load=load)

while verif:
    if b1.loop % b1.loops_para_gravar == 0 and b1.loop > 0:
        b1.run(save=True)
        verif = False

    else:
        b1.run()