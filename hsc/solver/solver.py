import pathlib

import dolfinx
import numpy as np
import ufl
from mpi4py import MPI

from hsc.domain_properties import Description
from hsc.mesh import MeshBuilder

from .adiabatic_absorber import AdiabaticAbsorber
from .util import get_mesh

from dolfinx.fem.petsc import LinearProblem  # isort: skip


class HelmholtzSolver:
    def __init__(self, out_dir: pathlib.Path, element):
        self.out_dir = out_dir
        self.element = element

    def __call__(self, description: Description):
        # MESH
        mesh_path = self.out_dir.joinpath(f"{description.unique_id}_mesh.msh")
        mesh_builder = MeshBuilder(description, mesh_path)
        mesh_builder.build()
        msh, ct, ft = get_mesh(mesh_path, comm=MPI.COMM_SELF)

        # Define function space
        v = dolfinx.fem.FunctionSpace(
            msh, ufl.FiniteElement("Lagrange", msh.ufl_cell(), 2)
        )
        v_plot = dolfinx.fem.FunctionSpace(
            msh, ufl.FiniteElement("Lagrange", msh.ufl_cell(), 1)
        )

        # define domain parameters
        p0 = 1.0
        x_tilde = dolfinx.fem.Function(v)
        alpha = dolfinx.fem.Function(v)
        sigma = AdiabaticAbsorber(description)

        p_i = dolfinx.fem.Function(v)  # incident wave

        dx = ufl.Measure("dx", msh, subdomain_data=ct)
        dx_domain = (
            dx(description.indices["left_side"])
            + dx(description.indices["crystal_domain"])
            + dx(description.indices["right_side"])
        )
        dx_pml = dx(description.indices["absorber"])

        # Define variational problem
        p_s = ufl.TrialFunction(v)
        xi = ufl.TestFunction(v)

        p_sol = dolfinx.fem.Function(v)
        p_sol.name = "p"

        # Start writer
        filename = self.out_dir.joinpath(f"{description.unique_id}_solution.xdmf")
        writer = dolfinx.io.XDMFFile(
            MPI.COMM_SELF, filename, "w", encoding=dolfinx.io.XDMFFile.Encoding.HDF5
        )
        writer.write_mesh(msh)

        for i, (k0, f) in enumerate(zip(description.ks, description.frequencies)):
            x_tilde.interpolate(lambda x: 1 + sigma.eval(x) / (1j * k0))
            j = ufl.as_matrix(((x_tilde, 0, 0), (0, 1, 0), (0, 0, 1)))
            j_inv = ufl.inv(j)
            j_det = ufl.det(j)

            alpha.interpolate(
                lambda x: 1 / (1 + 1j * sigma.eval(x) / k0 * description.c)
            )

            p_i.interpolate(lambda x: p0 * np.exp(1j * k0 * x[0]))

            # assemble problem
            lhs = (
                ufl.inner(ufl.grad(p_s), ufl.grad(xi)) - k0**2 * ufl.inner(p_s, xi)
            ) * dx_domain

            lhs += (ufl.inner(j_inv * ufl.grad(p_s), j_inv * ufl.grad(xi))) * dx_pml
            lhs -= (-(k0**2) * ufl.inner(p_s, xi) * j_det) * dx_pml

            rhs = (
                -ufl.inner(ufl.grad(p_i), ufl.grad(xi)) + k0**2 * ufl.inner(p_i, xi)
            ) * dx

            # compute solution
            problem = LinearProblem(
                lhs,
                rhs,
                u=p_sol,
                petsc_options={
                    "ksp_type": "preonly",
                    "pc_type": "cholesky",
                    "pc_factor_mat_solver_type": "mumps",
                },
            )
            problem.solve()

            p_sol.x.array[:] = p_sol.x.array[:] + p_i.x.array[:]

            # write solution
            out_function = dolfinx.fem.Function(v_plot)
            out_function.interpolate(p_sol)
            writer.write_function(out_function, f)

        # Close writer
        writer.close()

        # cleanup
        mesh_builder.delete_msh_files()
