The goal of geophysical inversions is to image the subsurface of the earth (without digging anything up!!).
The realization of this goal can be hard because it requires a deep understanding in several disciplines
including geology, physics, math, and computer science. Due to the diversity required to complete an inversion,
geophysical researchers are susceptible to get 'lost' on their way to realizing their **geophysical ideas**.
Researchers are always having new ideas; however, most of them are not realized in the world, because of the
difficulties in communication among many disciplines in an organized way.

Ideas are fickle and, in my experience, only stick with you for a short amount of time with any sort of clarity.
Ideas need to be incubated in the proper environment if they are to be realized in the world. The motivation behind
SimPEG (Simulation and Parameter Estimation in Geophysics) is to provide a toolbox and a framework such that
geophysical researchers can realize their ideas quickly and efficiently. In this way we hope that researchers
won't lose the momentum of their geophysical curiosity and perhaps realize a few more ideas!

![Winding Path](/img/nudging-geophysics/a-winding-path.png)

In order to show some of the capabilities of SimPEG we will show an example of simulating physics, which is a
fundamental step in any geophysical inversion. Sometimes, geophysicists go to the field and hook up a battery
to the ground. They then use a voltmeter to measure the response from the earth on the ground surface.

![DC Resistivity Survey](/img/nudging-geophysics/dc-survey.png)

This geophysical survey called a direct current (DC) resistivity survey, and it is one of the most used
geophysical methods in environmental engineering and the mining industry. Amazingly, with the proper application
of geophysical inversions to the measured DC resistivity data, we can restore the resistivity distribution and
image the subsurface of the earth. In this example, we simulate the physics in DC resistivity survey, and show
how different disciplines including math, physics and computer science can be connected intuitively through
SimPEG's toolbox.

## Example: DC resistivity survey

```python
from SimPEG import Mesh, Utils, Solver
import scipy
%pylab inline
```

### Bring the earth into your computer and represent it as numbers: discretization (mesh)

```python
cs = 5
hx = np.ones(250)*cs
hy = np.ones(250)*cs
mesh = Mesh.TensorMesh([hx, hy], 'C0')
m = Mesh.TensorMesh([10, 10], 'CC')
fig, ax = plt.subplots(1,1, figsize = (5,5))
m.plotGrid(nodes=True, faces=True, centers=True, ax = ax)
ax.legend(('nodes', 'cell-center', 'x-face', 'y-face'), loc=1)
```

![A simple Mesh](/img/nudging-geophysics/a-mesh.png)

### Discipline #1: Maxwell's quations in steady state (Physics)

$$
\nabla \cdot \sigma \nabla \phi = -q
$$

### Discipline #2: In discretized space (Finite volume Discretization)

$$
\mathbf{A} = \mathbf{Div} \mathbf{diag}(\mathbf{Av}_{cc}^{F T}\mathbf{\sigma})\mathbf{Grad} \\
\mathbf{A}\phi = -\mathbf{q}
$$

### Discipline #3: Code

```python
Div = mesh.faceDiv
Grad = mesh.cellGrad
vol = mesh.vol
AvF2CC = mesh.aveF2CC
sigma = np.ones(mesh.nC)*1e-2
getA = lambda sigma: Div*(Utils.sdiag(AvF2CC.T*sigma))*Grad
A = getA(sigma)
q = np.zeros(mesh.nC)
inds = Utils.closestPoints(mesh,[[-400, 1200],[400,1200]])
q[inds] = [-1., +1]
```

Those three different disciplines including physics, math (discretization) and computer science (code) can be
intuitively connected through SimPEG's toolbox. In my experience, this is awesome to test your rough ideas really fast.


## Compute responses for homogeneous earth

```python
phi_half = Solver(A)*-q
fig, ax = plt.subplots(1,1, figsize=(10,7))
dat = mesh.plotImage(Grad*(phi_half), vType='F', view = 'vec', streamOpts={'color': 'w'}, ax=ax)
cb = plt.colorbar(dat[0])
cb.set_label('Electric field (V/m)', fontsize=14)
```

![Homogeneous Earth](/img/nudging-geophysics/dc-homogeneous.png)


## Compute responses for *heterogeneous* earth

Perhaps from a python embedded in a resistive circle?

```python
img = scipy.misc.imread('SciPy_2014.png')
sigma_scipy = Utils.mkvc(img[:,:,0].astype(float))*1e-2 + 1e-2
fig, ax = plt.subplots(1,1, figsize=(10,7))
dat = mesh.plotImage(sigma_scipy,ax=ax)
cb = plt.colorbar(dat[0])
cb.set_label('Conductivity (S/m)', fontsize=14)
```

![Python in the earth](/img/nudging-geophysics/a-strange-earth.png)

```python
A = getA(sigma_scipy)
phi_scipy = Solver(A) * -q
fig, ax = plt.subplots(1,1, figsize=(10,7))
# dat = mesh.plotImage(phi, ax=ax)
dat = mesh.plotImage(Grad*(phi_scipy), vType='F', view = 'vec', streamOpts={'color': 'w'}, ax=ax)
cb = plt.colorbar(dat[0])
cb.set_label('Electric field (V/m)', fontsize=14)
```

![Heterogeneous Earth](/img/nudging-geophysics/dc-strange.png)

Look some distortions in the electric field of the earth due to a python! By measuring this perturbed electric
fields on the surface, we can potentially recover conductivity distribution of the earth. Doing a geophysical
inversion is still a bit more work (maybe for the next blog article?), but simulating the fields is a crucial
first step! The goal of SimPEG is that you can move fast, and the process is interactive so you can get rapid
feedback on your ideas. There might not actually be pythons is the subsurface, but it is good that it doesn't
take too long to check...!

This article is written for 2014 AGU Fall Meeting.
