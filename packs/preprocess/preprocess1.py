from .. import directories as direc
import numpy as np

class Preprocess1:

    def set_saturation_regions(self, M):

        centroids = M.data.centroids[direc.entities_lv0[3]]
        n = len(centroids)

        for reg in direc.data_loaded[direc.names_data_loaded_lv0[4]]:
            d0 = direc.data_loaded[direc.names_data_loaded_lv0[4]][reg]
            tipo = d0['type']
            value = d0['value']

            if tipo == direc.types_region_for_saturation[0]:
                tamanho_variavel = len(M.data.variables[M.data.variables_impress['saturation']])
                data = np.repeat(value, tamanho_variavel)
                M.data.variables[M.data.variables_impress['saturation']] = data

            elif tipo == direc.types_region_for_saturation[1]:
                type1 = d0['type1_well']
                type2 = d0['type2_well']
                tipos = [type1, type2]
                all_wells = []
                all_values = []

                for tipo in tipos:
                    if tipo == 'dirichlet':
                        wells = M.contours.datas['ws_p'].flatten()
                    elif tipo == 'neumann':
                        wells = M.contours.datas['ws_q'].flatten()
                    elif tipo == 'injector':
                        wells = M.contours.datas['ws_inj'].flatten()
                    elif tipo == 'producer':
                        wells = M.contours.datas['ws_prod'].flatten()
                    else:
                        continue

                    all_wells.append(wells)
                    all_values.append(np.repeat(value, len(wells)))

                all_wells = np.array(all_wells).flatten()
                all_values = np.array(all_values).flatten()
                M.data.variables[M.data.variables_impress['saturation']][all_wells] = all_values







