When solving any math or physics problem, there are usually a few tricks that can take you a long ways. Some of the favorites are: multiplying by 1 (or the identity), adding zero, and breaking things up in to sums (i.e. 2 = a+b, where a=1). I am sure these will be recurring themes among our articles. Here, I am going to spend some time on last point in the context of the frequency domain Maxwell's equations. In this case, 2 = a+b goes by the name of Primary-Secondary. I will develop this for the frequency domain electromagnetic (FDEM) problem, but keep in mind that it is quite general.

# Maxwell

The FDEM is governed by Maxwell's equations, which, under the the quasi-static approximation are given by:

$$
\nabla \times \vec{E} + i \omega \vec{B} = \vec{S}_m
$$

$$
\nabla \times \mu^{-1} \vec{B} - \sigma \vec{E} = \vec{S}_e
$$

where $\vec{E}$ is the electric field, $\vec{B}$ is the magnetic flux density, $\mu$ is the magnetic permeability, $\sigma$ is the electric conductivity, $\omega = 2 \pi f$ is the angular frequency and $\vec{S}_m$ and $\vec{S}_e$ are the magnetic and electric source current densities, respectively (see for example: Ward and Hohmann, 1988).

There are a large number of options for primary-secondary: 2 = a + b leaves the door wide open... there are actually an infinite number of possibilities, but not all of them will be useful. I will give you a couple of examples, and hopefully that will give you a feel for where this can be handy.


# Primary-Secondary for conductivity

All we are going to do here is define

$$\sigma = \sigma_p + \sigma_s$$
$$\vec{E} = \vec{E}_p + \vec{E}_s$$
$$\vec{B} = \vec{B}_p + \vec{B}_s$$

where the superscript $p$ indicates "primary" and $s$ indicates secondary, for now we will treat them as arbitrary (stick with me for a minute...), then

$$
\nabla \times (\vec{E}_p + \vec{E}_s) + i \omega (\vec{B}_p + \vec{B}_s) = \vec{S}_e
$$

$$
\nabla \times \mu^{-1} (\vec{B}_p + \vec{B}_s) - (\sigma_p + \sigma_s) (\vec{E}_p + \vec{E}_s) = \vec{S}_m
$$

We haven't actually done anything yet. To make this a useful approach, we need to define our primary. We are free to choose anything, the idea here is that we gain something (ie. easier or faster to compute, or the ability to take advantage of an analytical solution), so a useful choice turns out to be choosing a primary which satisfies:

$$
\nabla \times \vec{E}_p + i \omega \vec{B}_p= \vec{S}_m
$$

$$
\nabla \times \mu^{-1} \vec{B}_p - \sigma_p \vec{E}_p = \vec{S}_e
$$

where $\sigma_p$ is some simpler model than $\sigma$. For instance, $\sigma_p$ may be chosen to describe a half-space or 1-D model, where we have an analytical solution for the above set of equations. Using these, we can then find a set of equations for $\vec{E}_s$, $\vec{B}_s$. Starting from:

$$
\nabla \times (\vec{E}_p + \vec{E}_s) + i \omega (\vec{B}_p + \vec{B}_s) = \vec{S}_m
$$

$$
\nabla \times \mu^{-1} (\vec{B}_p + \vec{B}_s) - (\sigma_p + \sigma_s) (\vec{E}_p + \vec{E}_s) = \vec{S}_e
$$

we expand it out:

$$
\nabla \times \vec{E}_p + \nabla \times \vec{E}_s + i \omega \vec{B}_p + i \omega \vec{B}_s = \vec{S}_m
$$

$$
\nabla \times \mu^{-1} \vec{B}_p + \nabla \times \mu^{-1} \vec{B}_s - \sigma_p \vec{E}_p - \sigma_s \vec{E}_p - (\sigma_p + \sigma_s) \vec{E}_s = \vec{S}_e
$$

and use our definition of the primary:

$$
\nabla \times \vec{E}_s + i \omega \vec{B}_s = 0
$$

$$
\nabla \times \mu^{-1} \vec{B}_s - (\sigma_p + \sigma_s) \vec{E}_s = \sigma_s \vec{E}_p
$$

which is a system of equations in the secondary fields with the source $\sigma_s \vec{E}_p$. I am going to take one more step, and use the original definition of $\sigma = \sigma_p + \sigma_s$:

$$
\nabla \times \vec{E}_s + i \omega \vec{B}_s = 0
$$

$$
\nabla \times \mu^{-1} \vec{B}_s - \sigma \vec{E}_s = (\sigma - \sigma_p) \vec{E}_p
$$

So what we have done is replace our source term with this new source: $(\sigma - \sigma_p)\vec{E}_p$ that is nonzero only where there is a difference between the true conductivity model $\sigma$ and the conductivity model we captured in the primary $\sigma_p$.


# Zero Frequency Source

Often when using a magnetic dipole source, it is useful to use a zero-frequency primary, then we can define the source analytically as a curl of a vector potential. This ensures that the divergence of the magnetic field is zero (ie. we are not numerically creating magnetic monopoles) if we are using a mimetic discretization. We start with:

$$
\nabla \times \vec{E} + i \omega \vec{B} = 0
$$

$$
\nabla \times \mu^{-1} \vec{B} - \sigma \vec{E} = \vec{S}_e
$$

Here, we choose a primary such that
$$
\nabla \times \mu^{-1} \vec{B}_p = \vec{S}_e
$$

$$
\nabla \cdot \vec{B}_p = 0
$$

and $\vec{E}_p = 0$

Since $\vec{B}_p$ is divergence-free, it can be described by the curl of a vector potential (the divergence of a curl is zero),

$$
\vec{B}_p = \nabla \times \vec{A}
$$

For the case of a static magnetic dipole in a space with homogeneous permeability $\mu$, $\vec{A}$ is give by:

$$
\vec{A} = \frac{\mu}{4 \pi} \frac{\vec{m} \times \hat{r}}{r^2}
$$

See for example: Griffiths, 1999 section 5.4

Using this, we define $\vec{A}$ everywhere on the mesh and take the discrete curl to get the primary magnetic field. When using a mimetic discretization, the discrete divergence of a discrete curl is identically zero, so we preserve the divergence-free condition on $\vec{B}_p$.

Now to set-up the secondary problem, we play the same game as before and split up the fields in Maxwell's equations into primary and secondary:

$$
\nabla \times \vec{E} + i \omega (\vec{B}_p+\vec{B}_s)  = 0
$$

$$
\nabla \times \mu^{-1} (\vec{B}_p+\vec{B}_s) - \sigma \vec{E} = \vec{S}_e
$$

using the definition of the primary

$$
\nabla \times \vec{E} + i \omega \vec{B}_s  = -i \omega \vec{B}_p
$$

$$
\nabla \times \mu^{-1} \vec{B}_s - \sigma \vec{E} = 0
$$

That is, we have a frequency-dependent magnetic source term for the secondary problem.


## Other applications

A primary-secondary approach is often used in Magnetotellurics (MT) to simplify the boundary conditions. If performing a full 3D simulation for MT, the boundary conditions drive the system, and must be accounted for in the definition of the discrete differential operators. However, primary-secondary approach can be used to allow natural boundary conditions (ie. the fields have sufficiently decayed before encountering the boundary) to be employed. A 1D background is often assumed for the primary, and the primary fields can be computed analytically using a propagator matrix approach (see Ward and Hohmann, 1988 page 194), or with a 1D forward simulation. The source term is found using the Primary-Secondary approach for conductivity shown above.

Recently, I have been looking at using Primary-Secondary in settings with steel-cased wells. If the source is inside of the well, and the geologic setting is a layered 1D earth, then the problem is cylindrically symmetric and a 2D problem can be solved. However, if there are 3D structures, a primary-secondary approach can be used: solve the cylindrically symmetric problem first, and use these as a primary for the 3D problem. If you want to know more... shameless self-plug: I will be presenting at SEG in New Orleans on Tuesday, October 20 at 9:45 in the Borehole Geophysics 1 session.


## In summary

We have broken the problem up into two: the primary and the secondary. The primary fields serve as a source for the secondary, thus connecting the two problems. Breaking this problem up in to two steps affords us some freedom as to how we choose to solve each of these problems. It is note necessarily the approach for every problem, but where symmetry can be exploited or analytics employed, it can prove to be a useful approach.
