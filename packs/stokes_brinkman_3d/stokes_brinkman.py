import numpy as np
from packs.stokes_brinkman_3d.assembly import assembly
from packs.preprocess.preprocess_stokes_brinkman import preprocess_stokes
from packs.solvers.solvers_pyamg import solver_amg
from packs.solvers.solvers_trilinos.solvers_tril import solverTril
import pyamg
import scipy
import gc
import time
class stokes_solver:
    def __init__(self,M):

        # print(gc.is_tracked(M))
        prep_sb=preprocess_stokes(M)
        assembled_matrices=assembly.global_assembly(prep_sb,M)
        self.M, self.lhs = assembled_matrices.M
        self.rhs= assembled_matrices.rhs
        # self.M[prep_sb.nv:,prep_sb.nv:]=np.identity(len(M.faces.internal))
        self.sol=self.solve(self.M,self.rhs, self.lhs, prep_sb)
        np.savetxt("results/mat.csv",self.M,delimiter=",")
        # np.save("results/b_sol.npy",self.sol)

        # sol_sb=np.load("results/b_sol.npy")

        # self.erro=abs(self.sol-sol_sb)


        self.write_output(prep_sb, M)
        

    def solve(self,Mat, rhs, lhs, prep_sb):
        Mat[0]=np.zeros(prep_sb.nv+prep_sb.nfi)
        Mat[0][0]=1
        Mat[prep_sb.nv-1]=np.zeros(prep_sb.nv+prep_sb.nfi)
        Mat[prep_sb.nv-1][prep_sb.nv-1]=1#
        t1=time.time()
        sol=np.linalg.solve(self.M,self.rhs)
        print(time.time()-t1,"numpy")
        t2=time.time()
        sol3=scipy.sparse.linalg.spsolve(lhs,rhs)
        print(time.time()-t2,"scipy")
        '''
        lhs=lhs.tolil()

        lhs[0]=np.zeros(prep_sb.nv+prep_sb.nfi)
        lhs[0,0]=1
        lhs[prep_sb.nv-1]=np.zeros(prep_sb.nv+prep_sb.nfi)
        lhs[prep_sb.nv-1,prep_sb.nv-1]=1#
        lhs.toarray()==Mat

        sol2=solver_amg.SolverAMG().smoothed_aggregation_solver(lhs.tocsr(),self.rhs.T,10**-40)
        sol3=scipy.sparse.linalg.spsolve(lhs,rhs)

        ml = pyamg.smoothed_aggregation_solver(lhs.tocsr())
        sol4 = ml.solve(rhs, tol=1e-10)
        sol5 = solverTril().solve_linear_problem(lhs.tocsr(),rhs)'''

        return sol

    def write_output(self,prep_sb,M):
        print(self.sol)
        N=len(M.volumes.all)+len(M.faces.internal)
        nx=len(prep_sb.fx)
        ny=len(prep_sb.fy)
        nz=len(prep_sb.fz)
        volumes=M.volumes.all
        M.pressure[volumes]=self.sol[volumes]
        M.velocity[prep_sb.fx]=np.array([self.sol[prep_sb.nv:prep_sb.nv+nx],np.zeros(nx),np.zeros(nx)]).T
        M.velocity[prep_sb.fy]=np.array([np.zeros(ny),self.sol[prep_sb.nv+nx:prep_sb.nv+nx+ny],np.zeros(ny)]).T
        M.velocity[prep_sb.fz]=np.array([np.zeros(nz),np.zeros(nz),self.sol[prep_sb.nv+nx+ny:prep_sb.nv+nx+ny+nz]]).T

        # M.erro_p[volumes]=self.erro[volumes]
        #
        # M.erro_v[prep_sb.fx]=np.array([self.erro[prep_sb.nv:prep_sb.nv+nx],np.zeros(nx),np.zeros(nx)]).T
        # M.erro_v[prep_sb.fy]=np.array([np.zeros(ny),self.erro[prep_sb.nv+nx:prep_sb.nv+nx+ny],np.zeros(ny)]).T
        # M.erro_v[prep_sb.fz]=np.array([np.zeros(nz),np.zeros(nz),self.erro[prep_sb.nv+nx+ny:prep_sb.nv+nx+ny+nz]]).T

        v=M.core.mb.create_meshset()
        M.core.mb.add_entities(v,M.core.all_volumes)
        M.core.mb.write_file("results/solution_volumes.vtk",[v])

        f=M.core.mb.create_meshset()
        M.core.mb.add_entities(f,M.core.all_faces)
        M.core.mb.write_file("results/solution_faces.vtk",[f])
