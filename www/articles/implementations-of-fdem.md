This past week, I worked on implementing the H-J formulation of Maxwell's equations (in the Frequency Domain) in [simpegEM](https://github.com/simpeg/simpeg). So for this week's journal, I thought I would write about the 4 different approaches we have implemented for solving the FDEM problem.

## Two Formulations for Maxwell

Often, we work with the E-B formulation (under the quasi-static approximation - i.e. we ignore wave propagation):

$$
\nabla \times \vec{E} + i \omega \vec{B} = 0
$$

$$
\nabla \times \mu^{-1} \vec{B} - \sigma \vec{E} = \vec{J}_s
$$

where $\vec{E}$ is the electric field and $\vec{B}$ is the magnetic flux density. The physical properties are: magnetic permeability, $\mu$, and electrical conductivity, $\sigma$. The frequency dependence is captured by $\omega = 2\pi f$, and the source current density is $\vec{J}_s$. To get to the H-J formulation, we use the constitutive relations

$$
\vec{B} = \mu \vec{H}
$$

$$
\vec{J} = \sigma \vec{E}
$$

which relate the magnetic field and flux, and electric field and flux, respectively. The H-J formulation of Maxwell's equations is given by:

$$
\nabla \times \sigma^{-1} \vec{J} + i \omega \mu \vec{H} = 0
$$

$$
\nabla \times \vec{H} - \vec{J} = \vec{J}_s
$$

We now have two expressions for Maxwell's equations. Note that these two formulations are equivalent in the continuous world, but when we discretize, they are no longer equivalent.

## Where do we put things?

The physical properties, fields and fluxes need to live somewhere in a mesh. Lets assume we are using a tensor mesh. There are four types of real estate in a mesh: cell-centers, nodes, edges and faces.

![FV Real Estate](/img/finitevolrealestate)

It is convenient to consider physical properties to be in cell-centers, then their value occupies the volume of that cell (you can discretize them on nodes, but we are not going to get in to that here). In both formulations, we will put the physical properties in the cell centers; this is where the first difference arrives between the two formulations. The physical properties discretize we discretize are inverses of each other between the two formulations.

| Formulation       | Variables we Discretize     |
| ----------------- | ---------- | -------------- |
|  E-B formulation  | $\mu^{-1}$ | $\sigma$       |
|  H-J formulation  | $\mu$      | $\sigma^{-1}$  |

Both faces and edges are vector properties, they have a direction attached to them, so these are the locations where we will be putting the fluxes and fields. There are a couple of things that help us make this decision:

1. At cell boundaries, the physical property models may be discontinuous. When there is a discontinuity
    - the normal component of the flux and the tangential component of the field are continuous
    - the tangential component of the flux and the normal component of the field may be discontinuous
2. Fluxes are defined through a surface while fields can be defined at a point.

If we discretize fields on edges and fluxes on faces, both points are taken care of, and everything is happy and continuous:

| Formulation       | Edge       | Face           |
| ----------------- | ---------- | -------------- |
|  E-B formulation  | $\vec{E}$  | $\vec{B}$      |
|  H-J formulation  | $\vec{H}$  | $\vec{J}$      |

To sum up:

![FV Discretization](/img/ebjhdiscretizations)

## Discretized Equations

We use the mesh class in SimPEG to generate our operators including the edge-curl: $\mathbf{C}$ and the edge and face inner product matrices $\mathbf{M^e}_x$, $\mathbf{M^f}_x$.
I am going to gloss over some details here, referring you to the [documentation](http://docs.simpeg.xyz), and simply state the results.

<!-- TODO: add a useful reference (Eldad's book and our documentation?) -->

**E-B Discretization**

$$
\mathbf{C}\mathbf{e} + i\omega\mathbf{b} = 0
$$

$$
\mathbf{C}^T\mathbf{M^f_{\mu^{-1}}}\mathbf{b} - \mathbf{M^e_{\sigma}} \mathbf{e} = \mathbf{j_s}
$$


**H-J Discretization**

$$
\mathbf{C}^T \mathbf{M^f_{\sigma^{-1}} } \mathbf{j} + i \omega \mathbf{M^e_{\mu}} \mathbf{h} = 0
$$

$$
\mathbf{C}\mathbf{h} - \mathbf{j} = \mathbf{j_s}
$$


## Solving

Now to solve for our fields and fluxes! Instead of solving the first order system in each case, we eliminate a field or flux in each and solve a second order system.


### E-B Formulation

We have two options, 1) eliminate $\mathbf{b}$, and solve for $\mathbf{e}$ or 2) eliminate $\mathbf{e}$ and solve for $\mathbf{b}$. Both cases are implemented in simpegEM, so we will show both here.
<!-- I find looking at continuous operators useful in gaining intuition, so as in the following, I will include the continuous notation next to the discrete version.  -->


#### Solve for E (simpegEM.FDEM.ProblemFDEM_e)

Here, we eliminate $\mathbf{b}$ using

<!-- | Discrete | Continuous |
|---------------------------------------------------------| -->
<!-- | -->
$$
\mathbf{b} = -\frac{1}{i\omega} \mathbf{C}\mathbf{e}
$$
<!-- | $\vec{B} = -\frac{1}{i\omega} \nabla \times \vec{E}$ -->

giving a second order equation in $\mathbf{e}$

<!-- |  -->
$$
\left(\mathbf{C}^T\mathbf{M^f_{\mu^{-1}}} \mathbf{C} + i\omega\mathbf{M^e_{\sigma}}\right) \mathbf{e} = -i\omega\mathbf{j_s}
$$
<!-- $ | $\nabla \times \mu^{-1} \nabla \times \vec{E} + i \omega \sigma \vec{E} = -i \omega \vec{J}_s -->
<!-- | $\nabla \times \mu^{-1} \vec{B} - \sigma \vec{J}_s$ | -->

Once we discretize the source, $\mathbf{j_s}$, we can solve this for $\mathbf{e}$, and from that get $\mathbf{b}$ as well.


#### Solve for B (simpegEM.FDEM.ProblemFDEM_b)

Instead, we could eliminate $\mathbf{e}$ using

<!-- $ |  -->
$$
\mathbf{e} =  \mathbf{M^e_{\sigma}}^{-1} \mathbf{C}^T\mathbf{M^f_{\mu^{-1}}}\mathbf{b} - \mathbf{M^e_{\sigma}}^{-1}\mathbf{j_s}
$$
<!-- | \vec{E} =  \sigma^{-1} \nabla \times \mu^{-1} \vec{B} - \sigma^{-1}\vec{J}_s $ -->

and get a second order system in $\mathbf{b}$

<!-- $|  -->
$$
\left(\mathbf{C}\mathbf{M^e_{\sigma}}^{-1} \mathbf{C}^T\mathbf{M^f_{\mu^{-1}}} + i\omega\right)\mathbf{b} = \mathbf{C}\mathbf{M^e_{\sigma}}^{-1}\mathbf{j_s}
$$
 <!-- | $\nabla \times \sigma^{-1} \nabla \times \mu^{-1} \vec{B} + i\omega\vec{B} = \nabla\times\sigma^{-1}\vec{J}_s$ | -->

This is interesting: the right hand side depends on the model. This is fine if we simply want to solve the forward problem for $\mathbf{b}$, but it becomes a real pain in the neck when we want to do the inverse problem, where we need derivatives with respect to $\sigma$. We can do this, but it does involve more matrix multiplications. Another option is to change up the way we define our source using a Primary-secondary approach. We define $\mathbf{b} = \mathbf{b}^P + \mathbf{b}^S$, $\mathbf{e} = \mathbf{e}^P + \mathbf{e}^S$. The discrete equations in this case are:

$$
\mathbf{C}(\mathbf{e}^P + \mathbf{e}^S) + i\omega(\mathbf{b}^P+\mathbf{b}^S) = 0
$$

$$
\mathbf{C}^T \mathbf{M^f_{\mu^{-1}}} (\mathbf{b}^P + \mathbf{b}^S) - \mathbf{M^e_\sigma} (\mathbf{e}^P + \mathbf{e}^S) = \mathbf{j_s}
$$

We have some freedom in how we define the primary, but keep in mind that our goal is to choose a primary that simplifies the problem, so in this case, to simplify, it is beneficial to pick a primary that captures the source term. Here, we use a zero-frequency primary (ie. assume that the primary satisfies the static Maxwell's equations). This is a handy choice, for instance for a magnetic dipole source, when we have an analytical solution which is independent of the conductivity (Note: there is no free lunch. If the solution for the primary is not independent of the conductivity, the derivatives will still need to taken care of.)

$$
\mathbf{C}\mathbf{e}^P = 0
$$

$$
\mathbf{C}^T \mathbf{M^f_{\mu^{-1}}} \mathbf{b}^P - \mathbf{M^e_\sigma} \mathbf{e}^P = \mathbf{j_s}
$$

Using this, we have that,

$$
\mathbf{C} \mathbf{e}^S + i\omega\mathbf{b}^S = -i\omega\mathbf{b}^P
$$

$$
\mathbf{C}^T \mathbf{M^f_{\mu^{-1}}} \mathbf{b}^S - \mathbf{M^e_\sigma} \mathbf{e}^S = 0
$$

So our new source term is $-i\omega\mathbf{b}^p$. If we eliminate $\mathbf{e}^S$, we have a second order equation in $\mathbf{b}^S$:

$$
(\mathbf{C} \mathbf{M_\sigma^e}^{-1} \mathbf{C}^T \mathbf{M_{\mu^{-1}}^f} + i\omega)\mathbf{b}^S = - i\omega \mathbf{b}^P
$$

Which we solve for $\mathbf{b}^S$. We can either add back the primary or just work with the secondary in the inverse problem.

<!-- Since $$ \mathbf{C}\mathbf{e}^P = 0 $$, it can be described by the gradient of a potential. So long as the source term is divergence free

$$
\mathbf{C}^T \mathbf{M^f_{\mu^{-1}}} \mathbf{b}^P = \mathbf{j_s}
$$  -->

### H-J Formulation

We can play similar games with the H-J formulation.

#### Solve for J (simpegEM.FDEM.ProblemFDEM_j)

We eliminate $\mathbf{h}$ using

$$
\mathbf{h} = - \frac{1}{i\omega} \mathbf{M^e_{\mu}}^{-1} \mathbf{C}^T \mathbf{M^f_{\sigma^{-1}} } \mathbf{j}
$$

That gives us a second order equation in $\mathbf{j}$

$$
\left(\mathbf{C}\mathbf{M^e_{\mu}}^{-1} \mathbf{C}^T \mathbf{M^f_{\sigma^{-1}} } + i\omega\right) \mathbf{j} = - i\omega\mathbf{j_s}
$$


#### Solve for H (simpegEM.FDEM.ProblemFDEM_h)

Or, we can eliminate $\mathbf{j}$

$$
\mathbf{j} = \mathbf{C}\mathbf{h} - \mathbf{j_s}
$$

giving

$$
\left( \mathbf{C}^T \mathbf{M^f_{\sigma^{-1}} } \mathbf{C} + i \omega \mathbf{M^e_{\mu}} \right) \mathbf{h} = \mathbf{C}^T \mathbf{M^f_{\sigma^{-1}} }  \mathbf{j_s}
$$

We can either solve this outright, or again use the primary-secondary approach.



## Summary

Well there you have it: 4 different ways to solve Maxwell's equations in the frequency domain using a finite volume approach. And why look at 4 approaches? There are a few reasons: in both the E-B and H-J implementations, we have the option to use primary-secondary (or not) depending on the type of source we are dealing with. Also, between the E-B and H-J implementations, we change where things live. I am particularly interested in this point when we reduce the dimensionality of the problem and use a cylindrically symmetric implementation. In the 2D cylindrical mesh, the edges are circles and lie only in the horizontal plane, while faces are vertical and radial. So the field we model only has an azimuthal component, while the flux has a vertical and radial components. If we want to model a vertical magnetic dipole, then we expect the magnetic flux to have vertical and radial components (no azimuthal component), while the resulting electric field will have only an azimuthal component. In this scenario, we should use the E-B formulation since then $\mathbf{e}$ lives on the edges and $\mathbf{b}$ on the faces. However, if we wanted to inject current vertically, we need the current density $\mathbf{j}$ to be defined on faces and have the magnetic field $\mathbf{h}$ on edges. Depending on the source and problem you are looking at, there may be one approach that is more suitable than the others, and now you have all of them at your fingertips in [simpegEM](https://github.com/simpeg/simpeg).