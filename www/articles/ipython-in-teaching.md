Last fall I was a part of a TA team (along with Mr. Seogi Kang!) for my supervisor's undergrad geophysics course.
The course is targeted at geologists and engineers who my work with geophysicists over the course of their careers.
So the aim of much of the content, labs, assignments, etc. is to equip them with the tools to communicate with geophysicsist.
This year, we embarked on a fairly major overhaul. We wanted to (and are still working to) re-vamp the way much of the material was presented to make it more engaging for students.
It is an interesting platform to explore how we explain concepts rooted in physics without getting bogged down in the math.

It is actually pretty incredible how much information we can compress into a collection of symbols strung together to describe governing equations, but that is not the point of this course.
This group of students needs enough intuition to have an idea of where geophysical techniques may be useful for the applications they may encounter in their careers and meaningful conversation with a geophysicist.

Building intuition requires a place where you can ask *What if...?*, try something, and get an answer.
If you ask enough *What if...?*'s, you can get a feel for the physics occurring between the input and the result.
Numerical simulations are an extremely powerful tool for asking these types of questions.
But how do you give students access to these tools without the having them get stuck in the overhead of coding?: You make toys!

Enter the [IPython notebook](http://ipython.org/notebook.html) and the [interact widget](http://nbviewer.ipython.org/github/adrn/ipython/blob/master/examples/Interactive%20Widgets/Index.ipynb).
Early in the semester, we did a lab on constructing a normal incidence seismogram.
We started by having them investigate the connection between the relevant physical properties, density and seismic velocity, and the reflectivity series.
What physical property combinations make the refection coefficients to be positive?, negative?, zero?

![Step 1](/img/ipython-in-teaching/IPython-Seismic-Step1.png)

These reflection coefficients are given in depth, but a seismogram is measured in time. How do we make that translation?

![Step 2](/img/ipython-in-teaching/IPython-Seismic-Step2.png)

When we go out and complete a seismic survey, we use a source wavelet. How do we get a seismogram? What happens if we make the input wavelet wider?

![Step 3](/img/ipython-in-teaching/IPython-Seismic-Step3.png)

Now we have walked through each of the pieces. Lets play with the inputs: the physical property model and wavelet and see what we get out. Can you construct models where we don't see a layer? What happens if you add noise?

![Step 4](/img/ipython-in-teaching/IPython-Seismic-Step4.png)

Check it out on github: [gpgTutorials/Seismic/SyntheticSeismogram](https://github.com/ubcgif/gpgTutorials/tree/master/Seismic/SyntheticSeismogram)


### Other reasons the notebook is a great teaching tool:

- It is easy to vary the level of detail exposed to students. For this lab, we hide pretty much everything in .py files, but it is easy to break out and include pieces of code that you want students to be exposed to.
- Regardless of how much you choose to show them in the notebook, the real deal is underneath. If students are curious, they can dig deeper; it is not packaged in a black-box that ends in .exe.
- and... open source for the win! There are great examples and tools out there that both reduce the workload on developers and provide some great ideas for explaining a variety of concepts.  


### What did the students think?

At the end of the term, we asked the students for feedback on a variety of aspects of the course. Overall, we recieved repeated feedback that the IPython tools we developed were among the more valueable tools they had access to in the course. I think we can be assured that by letting them play with the concepts, we are taking a step in the right direction. 
