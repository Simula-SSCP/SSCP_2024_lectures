{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# A contracting cube\n",
    "\n",
    "**Joakim Sundnes**\n",
    "\n",
    "Date: **June 27, 2023**\n",
    "\n",
    "\n",
    "## Model outline\n",
    "This notebook introduces a slight extension of the simple unit cube model introduced previously. The model will still be a simple unit cube, fixed at one end ($x=0$) and loaded with a pressure load (negative pressure, i.e. stretch) at the other end ($x=1.0$). The following two extensions will be introduced:\n",
    "* Replace the StVenant-Kirchhoff model with a model from Guccione et al (1995). \n",
    "* Add a time-varying active stress to the model"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### The material model by Guccione et al\n",
    "\n",
    "Soft biological tissues typically follow an exponential stress-strain relation. This relation was originally described by Fung, and has been implemented in a wide range of models for isotropic and anisotropic tissues. One of the most widely used material models for passive cardiac tissue is the model of Guccione et al from 1995. Several versions of the model have been used in the literature. We apply a transversely isotropic and nearly incompressible version, with strain energy given by:\n",
    "$$\n",
    "\\begin{align*}\n",
    "Q &= b_f E_{11}^2 + b_t (E_{22}^2 + E_{33}^2 + E_{23}^2 + E_{32}^2) + b_{fs}(E_{12}^2 + E_{21}^2 + E_{13}^2 + E_{31}^2),\\\\\n",
    "\\Psi &= \\frac{C}{2}(e^Q-1)+ \\kappa(J\\ln(J)-J+1)  .\n",
    "\\end{align*}\n",
    "$$\n",
    "Here $E_{ij}$ are the components of the Green-Lagrange strain tensor, defined relative to the local fiber orientation. Furthermore $J$ is the determinant of the deformation gradient $F$ ($J=1$ for an incompressible material), and $C,B_f,b_t,b_{fs}, \\kappa$ are material parameters. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Setting up the Fenics solver\n",
    "The bulk of the solver code will be identical to the first version of the unit cube. First, the usual imports, defining the mesh, the relevant function space and functions, and finally the Neumann and Dirichlet boundary conditions:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "from fenics import *\n",
    "\n",
    "# Optimization options for the form compiler\n",
    "parameters[\"form_compiler\"][\"cpp_optimize\"] = True\n",
    "parameters[\"form_compiler\"][\"representation\"] = \"uflacs\"\n",
    "parameters[\"form_compiler\"][\"quadrature_degree\"] = 4\n",
    "\n",
    "\n",
    "# Setup the mesh and the function space for the solutions\n",
    "mesh = UnitCubeMesh(4,4,4)\n",
    "V = VectorFunctionSpace(mesh, \"Lagrange\", 2)\n",
    "\n",
    "\n",
    "# Define functions\n",
    "v  = TestFunction(V)             # Test function\n",
    "u  = Function(V)                 # Displacement from previous iteration\n",
    "\n",
    "# Mark boundary subdomains\n",
    "left =  CompiledSubDomain(\"near(x[0], side) && on_boundary\", side = 0.0)\n",
    "right = CompiledSubDomain(\"near(x[0], side) && on_boundary\", side = 1.0)\n",
    "\n",
    "boundary_markers = MeshFunction(\"size_t\", mesh,mesh.topology().dim() - 1)\n",
    "boundary_markers.set_all(0)\n",
    "left.mark(boundary_markers, 1)\n",
    "right.mark(boundary_markers, 2)\n",
    "\n",
    "# Redefine boundary measure\n",
    "ds = Measure('ds',domain=mesh,subdomain_data=boundary_markers)\n",
    "\n",
    "# Define Dirichlet boundary (x = 0 or x = 1)\n",
    "clamp = Constant((0.0, 0.0, 0.0))\n",
    "bc = DirichletBC(V, clamp, left)\n",
    "bcs = [bc]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, we turn to defining the mechanics problem. The following code cell is identical to the exercise from yesterday, and goes through the following steps:\n",
    "* Define the relevant kinematics\n",
    "* Define the strain energy function\n",
    "* Define the weak form, including the boundary conditions defined above\n",
    "* Solve the problem with a for loop, gradually increasing the load\n",
    "* Store the solution for plotting in Paraview, and plot the displacement in a single point\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "tags": [
     "hide-input",
     "hide-output"
    ]
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "No Jacobian form specified for nonlinear variational problem.\n",
      "Differentiating residual form F to obtain Jacobian J = F'.\n",
      "Solving nonlinear variational problem.\n",
      "  Newton iteration 0: r (abs) = 8.968e-01 (tol = 1.000e-10) r (rel) = 1.000e+00 (tol = 1.000e-09)\n",
      "  Newton iteration 1: r (abs) = 5.029e-01 (tol = 1.000e-10) r (rel) = 5.608e-01 (tol = 1.000e-09)\n",
      "  Newton iteration 2: r (abs) = 5.571e-02 (tol = 1.000e-10) r (rel) = 6.212e-02 (tol = 1.000e-09)\n",
      "  Newton iteration 3: r (abs) = 3.827e-03 (tol = 1.000e-10) r (rel) = 4.267e-03 (tol = 1.000e-09)\n",
      "  Newton iteration 4: r (abs) = 2.212e-05 (tol = 1.000e-10) r (rel) = 2.466e-05 (tol = 1.000e-09)\n",
      "  Newton iteration 5: r (abs) = 1.500e-09 (tol = 1.000e-10) r (rel) = 1.673e-09 (tol = 1.000e-09)\n",
      "  Newton iteration 6: r (abs) = 2.243e-16 (tol = 1.000e-10) r (rel) = 2.501e-16 (tol = 1.000e-09)\n",
      "  Newton solver finished in 6 iterations and 6 linear solver iterations.\n",
      "No Jacobian form specified for nonlinear variational problem.\n",
      "Differentiating residual form F to obtain Jacobian J = F'.\n",
      "Solving nonlinear variational problem.\n",
      "  Newton iteration 0: r (abs) = 3.455e-01 (tol = 1.000e-10) r (rel) = 1.000e+00 (tol = 1.000e-09)\n",
      "  Newton iteration 1: r (abs) = 2.187e-01 (tol = 1.000e-10) r (rel) = 6.331e-01 (tol = 1.000e-09)\n",
      "  Newton iteration 2: r (abs) = 9.950e-03 (tol = 1.000e-10) r (rel) = 2.880e-02 (tol = 1.000e-09)\n",
      "  Newton iteration 3: r (abs) = 1.126e-04 (tol = 1.000e-10) r (rel) = 3.258e-04 (tol = 1.000e-09)\n",
      "  Newton iteration 4: r (abs) = 1.776e-08 (tol = 1.000e-10) r (rel) = 5.142e-08 (tol = 1.000e-09)\n",
      "  Newton iteration 5: r (abs) = 2.652e-15 (tol = 1.000e-10) r (rel) = 7.677e-15 (tol = 1.000e-09)\n",
      "  Newton solver finished in 5 iterations and 5 linear solver iterations.\n",
      "No Jacobian form specified for nonlinear variational problem.\n",
      "Differentiating residual form F to obtain Jacobian J = F'.\n",
      "Solving nonlinear variational problem.\n",
      "  Newton iteration 0: r (abs) = 2.972e-01 (tol = 1.000e-10) r (rel) = 1.000e+00 (tol = 1.000e-09)\n",
      "  Newton iteration 1: r (abs) = 6.529e-02 (tol = 1.000e-10) r (rel) = 2.197e-01 (tol = 1.000e-09)\n",
      "  Newton iteration 2: r (abs) = 7.136e-04 (tol = 1.000e-10) r (rel) = 2.401e-03 (tol = 1.000e-09)\n",
      "  Newton iteration 3: r (abs) = 3.764e-07 (tol = 1.000e-10) r (rel) = 1.266e-06 (tol = 1.000e-09)\n",
      "  Newton iteration 4: r (abs) = 1.606e-13 (tol = 1.000e-10) r (rel) = 5.403e-13 (tol = 1.000e-09)\n",
      "  Newton solver finished in 4 iterations and 4 linear solver iterations.\n",
      "No Jacobian form specified for nonlinear variational problem.\n",
      "Differentiating residual form F to obtain Jacobian J = F'.\n",
      "Solving nonlinear variational problem.\n",
      "  Newton iteration 0: r (abs) = 2.659e-01 (tol = 1.000e-10) r (rel) = 1.000e+00 (tol = 1.000e-09)\n",
      "  Newton iteration 1: r (abs) = 3.224e-02 (tol = 1.000e-10) r (rel) = 1.213e-01 (tol = 1.000e-09)\n",
      "  Newton iteration 2: r (abs) = 1.424e-04 (tol = 1.000e-10) r (rel) = 5.355e-04 (tol = 1.000e-09)\n",
      "  Newton iteration 3: r (abs) = 1.091e-08 (tol = 1.000e-10) r (rel) = 4.101e-08 (tol = 1.000e-09)\n",
      "  Newton iteration 4: r (abs) = 5.544e-15 (tol = 1.000e-10) r (rel) = 2.085e-14 (tol = 1.000e-09)\n",
      "  Newton solver finished in 4 iterations and 4 linear solver iterations.\n",
      "No Jacobian form specified for nonlinear variational problem.\n",
      "Differentiating residual form F to obtain Jacobian J = F'.\n",
      "Solving nonlinear variational problem.\n",
      "  Newton iteration 0: r (abs) = 2.426e-01 (tol = 1.000e-10) r (rel) = 1.000e+00 (tol = 1.000e-09)\n",
      "  Newton iteration 1: r (abs) = 1.913e-02 (tol = 1.000e-10) r (rel) = 7.884e-02 (tol = 1.000e-09)\n",
      "  Newton iteration 2: r (abs) = 4.374e-05 (tol = 1.000e-10) r (rel) = 1.803e-04 (tol = 1.000e-09)\n",
      "  Newton iteration 3: r (abs) = 8.025e-10 (tol = 1.000e-10) r (rel) = 3.308e-09 (tol = 1.000e-09)\n",
      "  Newton iteration 4: r (abs) = 6.490e-15 (tol = 1.000e-10) r (rel) = 2.675e-14 (tol = 1.000e-09)\n",
      "  Newton solver finished in 4 iterations and 4 linear solver iterations.\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Kinematics\n",
    "d = len(u)\n",
    "I = Identity(d)             # Identity tensor\n",
    "F = I + grad(u)             # Deformation gradient\n",
    "F = variable(F)\n",
    "C = F.T*F                   # the right Cauchy-Green tensor\n",
    "E = 0.5*(C - I)             # the Green-Lagrange strain tensor\n",
    "\n",
    "# Material parameters (Lamé parameters)\n",
    "mu    = 4.0  \n",
    "lmbda = 20.0  \n",
    "\n",
    "# The strain energy for the St-Venant Kirchhoff model:\n",
    "psi = lmbda / 2 * (tr(E)**2) + mu * tr(E * E)\n",
    "P = diff(psi, F)\n",
    "\n",
    "p_right = Constant(0.0) #the pressure load (zero for now)\n",
    "\n",
    "# Definition of the weak form:\n",
    "N = FacetNormal(mesh)\n",
    "Gext = p_right * inner(v, det(F) * inv(F) * N) * ds(2) #ds(2) = left boundary\n",
    "R = inner(P,grad(v)) * dx + Gext \n",
    "\n",
    "#Finally, we solve the problem for different loads, and plot the load vs displacement. \n",
    "# The middle point on the right boundary\n",
    "point0 = np.array([1.0,0.5,0.5])\n",
    "\n",
    "# Step-wise loading (for plotting and convergence)\n",
    "load_steps = 5\n",
    "target_load = 10.0\n",
    "loads = np.linspace(0, target_load, load_steps)\n",
    "\n",
    "d0 = np.zeros(3)                #displacement at point0\n",
    "disp = np.zeros(load_steps) #array to store displacement for all steps\n",
    "\n",
    "disp_file = XDMFFile(\"displacement/u.xdmf\")\n",
    "\n",
    "for step in range(load_steps):\n",
    "    # Stretch is a negative pressure\n",
    "    p_right.assign(-loads[step])\n",
    "    \n",
    "    #solve the problem:\n",
    "    solve(R == 0, u, bcs)\n",
    "    \n",
    "    #evaluate displacement at point defined above\n",
    "    u.eval(d0,point0)\n",
    "    disp[step] = d0[0]\n",
    "\n",
    "    disp_file.write_checkpoint(u, \"Displacement\", step, append=True)\n",
    "\n",
    "disp_file.close()\n",
    "\n",
    "#displacement on x-axis, load on y-axis\n",
    "plt.figure(1)\n",
    "plt.plot(disp,loads)\n",
    "plt.xlabel('Displacement of point (1.0, 0.5, 0.5)')\n",
    "plt.ylabel('Applied pressure load')\n",
    "\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1: Replace the StVenant-Kirchhoff material model\n",
    "Modify the code above to use the Guccione material model. You can implement the strain energy function directly yourself, or you can use an existing Python class which can be found here:\n",
    "\n",
    "* [Guccione model (1995)](./guccionematerial.py)\n",
    "\n",
    "The class supports both fully incompressible and nearly incompressible models. The key part is the function named `strain_energy`, which defines the strain energy as a function of the deformation gradient $F$. \n",
    "\n",
    "An important difference between the StVenant-Kirchhoff material and the Guccione model is that the Guccione model is anisotropic, meaning that the material properties are different in different directions. The material model therefore needs to know about the local tissue microstructure, i.e., the orientation of the fiber-, sheet- and sheet normal directions. For flexibility and generality, our material model class takes these vectors (or vector fields) as input parameters, as can be seen in the class' constructor.  \n",
    "\n",
    "In our simple unit cube, it is natural to define the fiber direction as parallel with the x-axis, the sheet direction parallel with the y-axis, and the normal direction parallel with the z-axis. Code for defining these vectors can look as follows:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Tissue microstructure\n",
    "f0 = as_vector([ 1.0, 0.0, 0.0 ])\n",
    "s0 = as_vector([ 0.0, 1.0, 0.0 ])\n",
    "n0 = as_vector([ 0.0, 0.0, 1.0 ])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Add these code lines and the necessary calls to the Guccione model class in the code above, to replace the StVenant-Kirchhoff material model with the Guccione material. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 2: Add active contraction\n",
    "\n",
    "Next, we want to add active contraction to the tissue cube. If we want to simulate a full cardiac cycle, a simple option would be to assign an active stress transient similar to the one output from the Rice et al model:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "import math\n",
    "\n",
    "force_amplitude=1.0\n",
    "#Ca_diastolic=0.09\n",
    "start_time=5, \n",
    "tau1=20 \n",
    "tau2=110\n",
    "t = np.linspace(0,1000,101)\n",
    "\n",
    "beta = -math.pow(tau1/tau2, -1/(1 - tau2/tau1)) + math.pow(tau1/tau2,\\\n",
    "        -1/(-1 + tau1/tau2))\n",
    "force = ((force_amplitude)*(np.exp((start_time - t)/tau1) -\\\n",
    "        np.exp((start_time - t)/tau2))/beta) \n",
    "\n",
    "#the following line implements the if test in numpy without a loop\n",
    "force = force*(t>=start_time)+ 0.0*(t<start_time)\n",
    "\n",
    "plt.plot(t,force)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "For now, we will keep things even simpler, and simply model the first phase of contraction by adding a linearly increasing active stress. For this case we consider an unloaded cube ($p=0$ on the right boundary). If you used the `GuccioneModel` class above to define the passive material properties, the active stress may be set in the function `set_active_stress`. \n",
    "\n",
    "A suitable definition of a linearly increasing active stress can be as follows:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step-wise loading (for plotting and convergence)\n",
    "active_steps = 6\n",
    "target_active = 5.0\n",
    "active = np.linspace(0,target_active,active_steps)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Add these lines and a suitable call to the `set_active_stress` function to the code above, to make the cube contract actively."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}