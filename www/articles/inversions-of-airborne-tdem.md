To demonstrate the inversion methodology using the [SimPEG](https://github.com/simpeg)
 framework and implementation, described in [SimPEG](https://github.com/simpeg), we use the airborne time domain electromagnetic (ATEM) method as a case study.
The ATEM method uses a transmitter loop, flown from either a helicopter or airplane, which transmits a waveform to excite the subsurface.
Data generally consist of measurements of the magnetic field or its time derivative on a sensor beneath the aircraft.
The ATEM forward problem requires considering both temporal and spatial discretizations,
and it is a conduit through which we can demonstrate many aspects the [SimPEG](https://github.com/simpeg)
 framework.

Following the collection and processing of the ATEM data, one often begins the inversion and interpretation process by formulating a series of 1D inversion. Each inversion assumes that the earth's structure is laterally uniform and varies only with depth.
In most cases, the earth's structure is more complex, having physical property variations vertically and laterally, and the 1D inversions will not be capable of producing a satisfactory model. However, this step can indicate the complex structures, as well as provide a measure of data quality. Such information can be used to estimate parameters for a 3D inversion, including mesh discretization and uncertainties assigned to the data. The 3D inversion is then used to recover a 3D electrical log-conductivity model of the surveyed region.

In order to realize a conventional ATEM inversion workflow within [SimPEG](https://github.com/simpeg)
,
we develop a time domain EM problem package [simpegEM](https://github.com/simpeg/simpegem) in this section. An overview of the 1D and 3D inversion implementations is shown in Figure 1.

### Governing equations

To build up the [simpegEM](https://github.com/simpeg/simpegem) package, we need to identify governing equations which
explain the observed ATEM data; thus, we start with the quasi-static Maxwell's equations in time domain

$$\nabla \times \vec{e} + \frac{\partial \vec{b}}{\partial t} = 0,  \nonumber  $$
$$\nabla \times \mu^{-1}\vec{b} -\vec{j} = \vec{j}_s, \nonumber  $$
$$\vec{b}(0, \vec{r}) = \vec{b}^0. $$

For brevity, we omit the spatial and temporal dependence of the electric field, $\vec{e} = \vec{e}(t, \vec{r})$, the magnetic flux density, $\vec{b} = \vec{b}(t, \vec{r})$, and the source current density, $\vec{j}_s = \vec{j}_s(t, \vec{r})$. The electrical conductivity $\sigma = \sigma(\vec{r})$ is assumed to be scalar function of space only and $\mu = \mu_0$ is assumed to be constant in space where $\mu_0$ is the magnetic permeability of vacuum space.

In order to compute the forward responses of the time domain system, we must discretize it both in time and in space.
To accomplish this, we use backward Euler for the time-discretization and finite volume method with weak formulation for the spatial-discretization.
Solving the discretized system provides the forward responses for the time domain EM system. We can compute the sensitivity of this system with respect to the model parameters. Detailed derivations are presented in [simpegem-documentation](http://simpegem.readthedocs.org/en/latest/api_TDEM_derivation.html) . Having defined the forward problem and sensitivities for the ATEM problem, we have defined the elements necessary for the Problem class.

![1D3Dframework](/img/inversions-of-airborne-tdem/Inv1Dand3D.png)

Figure 1. Overview of the implementation of a ATEM inversion in [SimPEG](https://github.com/simpeg)
. The 1D inversion utilizes a cylindrical mesh and the 3D inversion uses a 3D tensor mesh.

### Example

To initiate the exploration of an ATEM inversion workflow with SimPEG, we construct the 3D conductivity model shown in Figure 1, which includes two isolated conductive bodies and a resistive overburden.
The survey geometry includes 7 lines, each having 14 stations, as shown in Figure 1a, giving a total of 112 stations.
We use vertical magnetic dipole (VMD) source and measure $\frac{\partial b_z}{\partial t}$.
The transmitter and receiver are located 80 m and 30 m above the surface, respectively, and are horizontally coincident with zero lateral offset.
A step-off transmitter waveform is used, and 24 time channels between $1\times10^{-5}$s and $2\times10^{-3}$s are measured.
Prior to performing an inversion, we require data.
To generate synthetic data, $\mathbf{d}_\text{obs}$, we discretize the model on a 50$\times$50$\times$48 tensor mesh with 50$\times$50$\times$20m core cells, perform a forward calculation using the [simpegEM](https://github.com/simpeg/simpegem) package, and add 5% Gaussian noise.
In the following, we demonstrate a workflow to invert these ATEM data using the [simpegEM](https://github.com/simpeg/simpegem) package.

### 1D Inversion
We begin the inversion process by formulating a series of 1D inversions which assume a layered-earth structure.
Since we are using a VMD source, our system is cylindrically symmetric.
We take advantage of this symmetry by using a 2D cylindrical mesh to perform the forward modeling.
The 1D model is simply mapped onto the 2D mesh for the forward computation.
%1D structure of the model is maintained by assuming the conductivity model varies only with depth and does not vary laterally.
The 2D cylindrical mesh uses 50$\times$20m core cells, which is the same scale used in the 3D tensor mesh. The total number of cells in the domain is 55$\times$45, which is a much smaller system than the 3D tensor mesh. This allows the forward simulations to be run quickly.
An overview of the 1D inversion implemented in [SimPEG](https://github.com/simpeg)
 is shown in Figure 1.

Using the [simpegEM](https://github.com/simpeg/simpegem) package with a 2D cylindrical mesh, we invert the ATEM data at each station (shown in Figure 1a as black solid circles) for a 1D vertical model.
%to the observed ATEM data obtained at each station shown in Figure 1a as black solid circles.
After the separate inversions for each station are performed, we generate a stitched inversion result, which is a common visualization method for 1D inversions of ATEM data.
% The 1D inversions reached the designated target misfit for every station.
We show plan and section views of the 3D conductivity volume from these stitched 1D inversions in Figure 3.

These inversion results show evidence of conductive bodies, and the top of these bodies agree well with the true model.
However, when isolated bodies are embedded in the earth, 3D effects are significant, as evident by the artifacts present in our stitched conductivity model.
With these realizations, we move from a 1D layered earth assumption to a 3D inversion.
% These inversion results show that 1D inversion can reasonably delineate the layering of the earth.
% From the 1D inversion, we *** learn about layering, see evidence of conductive bodies, structure indicative of 3D effects in a 1D inversion.
%Therefore, now we need to release our 1D assumption to full 3D to restore reasonable 3D conductivity distribution.
Since we use same modules to compute ATEM responses for both mesh types in [simpegEM](https://github.com/simpeg/simpegem) package, this extension can be obtained by simply switching the mesh type from a series of 2D cylindrical meshes to a single 3D tensor mesh.

![3DconModela](/img/inversions-of-airborne-tdem/3dinv_xy_true.png)
![3DconModelb](/img/inversions-of-airborne-tdem/3dinv_yz_true.png)
Figure 2. Plan and section views of true conductivity model. Grey line contours show the discretization of the mesh. Black dots show the locations of stations; black dashed line indicates the horizontal line where we provide sectional view of the conductivity model.


![InvModels1Da](/img/inversions-of-airborne-tdem/1dinv_xy_pred.png)
![InvModels1Db](/img/inversions-of-airborne-tdem/1dinv_yz_pred.png)
Figure 3. Plan and section views of 3D conductivity volume estimated by 1D ATEM inversions. 1D conductivity models from each 1D inversion are stitched to generate 3D conductivity volume.

### 3D inversion
In a 3D inversion, we aim to recover a distributed log-conductivity model in 3D space.
Releasing the assumption of a 1D model increases the degrees of freedom and the non-uniqueness inherent in the inverse problem.
%thus, compared to 1D inversion, there are many more possible solutions which explain the observed data.
As such, proper definition of a regularization term in our objective function is one of the crucial factors in the success of this inversion.
%Previous statement made it sounds like no regularization was applied at all to the 1D inversion.
We use Tikhonov-style regularization including smallness and smoothness terms, as described in our paper with $\alpha_s = 0.01$ and $\alpha_x = \alpha_y = \alpha_z = 1$.
There are 112 receivers and each receiver has 24 time channels, the total number of the observed data is 2688.
We set the estimated uncertainty ($\epsilon$) using a percentage of the data magnitude plus a floor; for these data, we use $\epsilon = 0.05|d^{obs}|+10^{-5}\|d^{obs}\|_2$.

We note that, as defined, the choice of the factor of $10^{-5}$ in the noise floor depends on the number of data.
The target misfit is set as the number of observed data.
The initial trade-off parameter ($\beta$) is computed using
{%\iftoggle{finaldraft}{
\begin{equation}
    \beta_0 = c\frac{\|\mathbf{Jx}\|^2}{\|\mathbf{W_mx}\|^2},
\end{equation}
}
where $\bf x$ is a random vector and $c$ is an user-defined constant; in our 3D inversion we used $c=10^2$.
As an optimization routine, we use the inexact Gauss Newton method (cf. Dembo, 1982).
We use a a $\beta$-cooling scheme (cf. Nocedal, 1999; DougTutorial) where $\beta_{k+1} = \frac{1}{8}\beta_k$, and 2 inner Gauss-Newton iterations are performed between each $\beta$-cooling iteration.
An overview of the 3D ATEM inversion implementation in [SimPEG](https://github.com/simpeg)
 is shown in Figure 1.

The data misfit ($\phi_d$) and model regularization ($\phi_m$) curves are shown in Figure 4, where we see that the target misfit was reached at the 12^th^ iteration.
In Figure 4, we show a comparison of the observed and predicted data at $t=0.25$ms, which demonstrates an acceptable match.

We present plan and cross-section views of the recovered log-conductivity model after 12 iterations in Figure 5, respectively.
Compared to the 1D stitched inversions, the horizontal geometry of the two isolated bodies is better imaged, as shown in Figure 5.
Furthermore, by comparing Figure 3 and Figure 4, we recognize that some of the artifacts due to 3D effects in the 1D stitched inversions are no longer present.

![PredObsa](/img/inversions-of-airborne-tdem/3dinv_misfitcurve.png)
![PredObsb](/img/inversions-of-airborne-tdem/3dinv_obspred.png)

Figure 4. Three dimensional inversion results showing: inversion misfit curves where the red and black lines indicate data and model misfits, respectively; and comparisons of predicted and observed data at time, $t=0.25$ms, for the inversion at the target misfit.


![InvModels3Da](/img/inversions-of-airborne-tdem/3dinv_xy_pred.png)
![InvModels3Db](/img/inversions-of-airborne-tdem/3dinv_yz_pred.png)

Figure 5. Three dimensional inversion results showing: inversion misfit curves where the red and black lines indicate data and model misfits, respectively; and comparisons of predicted and observed data at time, $t=2.5$ms, for the inversion at the target misfit.

### Summary
In summary, using the ATEM problem as a case study we demonstrated a non-trivial inversion workflow for recovering an electrical conductivity model using the [SimPEG](https://github.com/simpeg)
 framework.
A preliminary model was found by carrying out many 1D inversions and stitching them together into the 3D volume. The final model was recovered by carrying out a full 3D inversion. Switching between these two inversions only required the user to change the mesh and definition of the model.
As demonstrated in this case study, the modularity and transparency of the [SimPEG](https://github.com/simpeg)
 framework allows targeted modifications throughout the iterative inversion process.