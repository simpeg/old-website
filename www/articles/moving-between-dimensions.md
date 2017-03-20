Electromagnetic (EM) methods are used to characterize the electrical
conductivity distribution of the earth. Since EM methods consider
time-varying fields, we typically treat EM in either the frequency
domain (FD) or the time domain (TD). Recently, due in part to
computational advances, EM geophysical surveys are increasingly being
simulated and inverted in 3D. However, the availability of computational
resources does not invalidate the use of lower dimensional formulations
and methods, which can be useful depending on the geological complexity
as well as the survey geometry. For example, we can treat the measured
EM data either in TD or FD, and a progressive procedure can be used to
invert these data, starting with 1D inversions, then moving to
multi-dimensional inversions. As such, we require a set of tools that
allow a geophysicists to easily move between dimensions and formulations
of the EM problem. This is the motivation behind the open source
software package SimPEG-EM which is part of a software ecosystem for
Simulation and Parameter Estimation in Geophysics (SimPEG). In this
study, we will share examples as well as our experience from creating a
range of simulation and inversion tools for EM methods that span
dimensions (1D, 2D and 3D) and apply TD formulations in a consistent
framework. The flexibility and consistency in our EM package allows us
to be methodical so that we have the capacity to tackle a spectrum of
problems in EM geophysics.

### What is the model?

Geophysical inversion is gearing towards recovering a model, which
usually considered as distribution of material property such as
electrical conductivity ($\sigma$). Machinery of the inversion is
finding a geologically reasonable model, which explain the observed
data. Governing equations of EM methods are Maxwell's equations in time
domain:

$$\nabla\times \vec{e} + \frac{\partial \vec{b}}{\partial t} = 0$$
$$\nabla\times \mu^{-1}\vec{b} -\sigma \vec{e} = \vec{j}_s$$

where $\vec{e}$ is electric field, $\vec{b}$ is magnetic
flux density, $\vec{j}$ is current density, $\vec{j}_s$ is
source current density, $\mu$ is magnetic permeability. Assuming
$\mu = \mu_0$ (magnetic permeability for vacuum space), we
consider electrical condcutivity ($\sigma$) as a principal
material property, and this can be 3D distribution:
$\sigma (x, y, z)$. We can excite this system by putting time
varying currents through $\vec{j}_s(t)$ term, and measure signals
from the the earth on arbitrary locations on surface. By discretizing
this PDE, we can compute forward responses which can be simply written
as

$$d^{pre} = F[\sigma]$$

where $F$ is Maxwell's operator and $d$ is EM responses at
receiver locations for corresponding transmitter. Assuming we know the
distribution of $\sigma$, the measured data can be written as

$$d^{obs} = F[\sigma]+noise$$

Using EM survey we can measure electromagnetic fields, which are the
observed data, and the goal of this survey is to recover distribution of
the conductivity. To perform this geophysical inversion process, a
generic question that we need to ask ourselves is *"What is the model?"*
in your inversion. Natural choice can be discretized 3D voxel of
conductivity: $\sigma (x, y, z)$, because we need this discretized
model to compute forward response. However, in most of EM inversions we
set our model parameter as $m (x, y, z) = log (\sigma(x, y, z))$,
considering the scale of variation in conductivity and positivity of the
conductivity. This clearly shows that model parameter in geophysical
inversion does not necessarily have to be same as distribution of
physical property. Therefore, we can define a mapping function, which
transform model parameter to distribution of physical property as

$$\sigma = \mathcal{M}(m)$$

where $\mathcal{M}$ is a model mapping function. Based on this,
above example can be written as $\sigma = \mathcal{M}(m) = e^{m}$.
This mapping function may completely decouple our model space of
inversion from the distribution of physical property. For example, our
model for inversion can be 1D or 2D, although EM response is computed in
3D space with 3D conductivity model (Figure 1a). In following article,
we will show treat suite of 1D, 2D and 3D EM inversions for seawater
intrusion model shown in Figure 1b using simpegEM package.

![Figure 1](/img/moving-between-dimensions/moving-dimensions-em-1.png)

Figure 1. (a) Conceptual diagram of 1D, 2D and 3D model. (b) Sea water
intrusion and geometry ground loop EM survey.

### Ground loop EM for seawater intrusion

In coastal area, sea water intrusion is a serious problem due to the
contamination of groundwater (Figure 2). One of the key to treat this
problem is to recognize the distribution of highly saturated zone by
seawater. Ground loop EM survey has been used to detect intruded
seawater, because of highly conductive nature of seawater. Figure 2
shows typical ground TEM geometry and conceptual geology near coastal
area. By putting time-varying current through the transmitter loop, we
excite the earth. Fundamental physics here is different from direct
current (DC) survey, given that we do not pump the electric charges to
the ground. Rather, we use EM induction phenomenon to excite the earth
in this case, which has high sensitivity on conductive structure. As a
geophyscist, we want to suggest possible region where we have serious
seawater intrusion. Therefore, for geophysicsts, recovering conductivity
distribution, which has high correlation with seawater saturation can be
a principal task.

### Anomalous responses from the intruded seawater

In order to realize that we first need to measure "meaningful data",
which has considerable information about intruded seawater, we need good
survey parameters. Figure 3a shows survey geometry of ground loop EM
survey. In this case we have two circular loops, which has 250 m radius.
We use simple layered earth model (1D) to make this analyses simple, and
ground loop source is circular thus, survey parameters are distance from
the center of the loop ($r$) and time. We perform two forward
responses due to the layered model with seawater layer and without
seawater layer, and compute amplitude ratio of them. Because we measure
vertical component of magnetic flux density ($b_z$), amplitude
ratio that we compute can be written as
$\frac{b_z[\sigma_{seawater}]}{b_z[\sigma_{background}]}$. In
Figure 3b, we provide amplitude ratio in 2D plane of which axes are time
and $r$. Contours on high amplitude ratios clearly shows measured
response at time range $10^{-3}$-$10^{-2}s$ are sensitive to
the seawater, and most of $r$ for corresponding time range.

![Figure 2](/img/moving-between-dimensions/moving-dimensions-em-2.png)

Figure 2. (a) Ground loop EM survey geometry. (b) Amplitude ratio of
vertical magnetic flux density with seawater and without seawater.

### Inversion methodology

We use gradient based inversion method, and optimize objective function
as

$$minimize \ \phi =  \phi_d(m) + \phi_m(m)$$

where $\phi_d$ = $\| d^{pred} - d^{obs}\|^2$ and
$\phi_m$ is related to model regularization. The core of our
optimization is sensitivity function:

$$J = \frac{\partial d^{pred}}{\partial m} = \frac{\partial d^{pred}}{\partial \sigma} \frac{\partial \sigma}{\partial m}$$

Recalling that we decoupled inversion model space ($m$) from
physical model space ($\sigma$) using mapping function
($\mathcal{M}(m)$), a simple requirement for us to implement
mapping in our inversion is to know derivative of our mapping function
($ $). Once we know this derivative for arbitrary mapping function, we
can proceed our geophysical inversion to recover the model that we
defined.

In our inversion, we may need suite of mappings. For instance, we use
$log(\sigma)$ as our model in the inversion, and do not want to
include discretized cells correspond to air region. Therefore, if we
apply 3D inversion with this, our mapping can be expressed as

$$\sigma = \mathcal{M}(m) = \mathcal{M_{exp}}(\mathcal{M_{active}}(m)))$$

where $\mathcal{M_{exp}}(\cdot)$ and
$\mathcal{M_{active}}(\cdot)$ indicate exponential and active
maps, respectively. Furthermore, if our inversion model is 1D or 2D
then, we need one additional map, which transform 1D or 2D model to 3D
model: $\mathcal{M_{1D~or~2D}}(\cdot)$. In this case, the
mapping for the 1D or 2D inversion can be expressed as

$$\sigma = \mathcal{M}(m) = \mathcal{M_{exp}}(\mathcal{M_{1~or~2D}}(\mathcal{M_{active}}(m))))$$

Based on that we know how to take derivative of this suite of mapping
functions, we can proceed our geophysical inversion (See mapping class
in SimPEG).

### 1D and 2D inversions


Conventionally for ground loop EM survey, we only measure one or two
profile lines of the data in the loop. And for the interpretation of
this data, we use 1D inversion, which assume layered-earth structure;
here 1D inversion for each datum is separate. After 1D inversion for
each datum we stitch recovered 1D conductivity model together to make a
2D-like section images. We generated synthetic ground TEM data set using
conductivity model shown in Figure 4 with survey geometry shown in
Figure 3a. Considering typical field configuration, we only used a
profline line in two loops for 1D and 2D inversions, which are expressed
as black solid dots in Figure 3a.

![Figure 3](/img/moving-between-dimensions/moving-dimensions-em-3.png)

Figure 3. Plan and section views of true conductivity model.

Recovered 1D stitched inversion model shown on the left panel of Figure
5 shows reasonable layering on the east-side. However, on the west-side
we can recognize artifacts in 1D stitched inversion due to 3D effect. On
the right panel of Figure 5a, we have also shown recovered conductivity
model from 2D inversion. This shows better horizontal resolution then 1D
inversion results, whereas layering show more spreaded distribution
compared 1D case. Comparison of observed and predicted data for these 1D
and 2D inversions are shown in Figure 5b. Although both predicted data
from 1D and 2D inversion results show reasonable match with the observed
data, we can recognize some discrepancy between observed and predicted
data, which may be caused by 3D effect that we cannot explain with 1D or
2D model.

![Figure 4](/img/moving-between-dimensions/moving-dimensions-em-4.png)

Figure 4. (a) 1D and 2D recovered models. (b) Observed and predicted
data for both inversions.

### 3D inversion

Distribution of seawater is in 3D thus, restoration of 3D conductivity
model can be one of the important tasks to characterize seawater
intruded region in the subsurface. For 1D and 2D inversions, we used a
profile line data, which were located in the loops. However, for 3D
inversion, having more measurement points aside from the center line may
be crucial to have reasonable sensitivity for 3D volume. We used all
receivers shown in Figure 3a. Figure 4a shows recovered conductivity
model from 3D inversion. Interface between fresh and seawater is nicely
imaged in both horizontal and vertical directions. We fit the observed
data well as shown in Figure 4b. We also provide cut-off 3D volume of
conductivity distribution in Figure 5.

![Figure 5](/img/moving-between-dimensions/moving-dimensions-em-5.png)

Figure 5. (a) 3D inversion results. (b) Observed and predicted data for
3D inversions.

![Figure 6](/img/moving-between-dimensions/moving-dimensions-em-6.png)

Figure 6. Cut-off 3D volume of true and recovered conductivity
distribution.

### Conclusions

Using mapping function in our geophysical inversion, we clearly
decoupled inversion model space from physical model space. This enables
us to set an arbitrary inversion model. We set three different inversion
models, which are 1D, 2D and 3D using mapping function, and performed
TEM inversions for seawater intrusion problem. Each inversion showed
reasonable recovered model based on the mapping for each case. Although
we treated limited subset of inversion models such as 1D, 2D and 3D,
general definition of mapping function that we suggested can be extended
to different inversion models. For instance, we can ask a specific
question: "where is the boundary of fresh and seawater?" in our
geophysical inversion using this mapping function. We believe this
separation of inversion model from physical property model will be a
powerful concept in the geophysical inversion, which allow us not only
to answer conventional question on our tasks in geophysics, but also ask
specific questions, which are more involved in other disciplines in
geoscience like certain geological feature of the earth system.

### If you want more stuff!

Check github repository if you want to know how we perform suite of
geophysical inversions:

[https://github.com/sgkang/AGU2014MovingDimensionsinEM.git](https://github.com/sgkang/AGU2014MovingDimensionsinEM.git)
