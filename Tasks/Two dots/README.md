# Encoding the dot
## KyivAIGroup, September 2018

Despite the recent advances, computer vision has many problems. We believe that we need to begin with the simple objects, before jumping to the complex visual intteligence. On the geometry classes we started with the simplest object - dot, and how it is described in space. Little bit more complex case is the two dots, that could become the endings of a line. Next - simple geometrical objects, triangels, squeres, perelelograms, circles. Together they can from 3d shapes. On the drawing classes people learn that to draw complex object, starting from the simple geometrical forms. Thus, learning to recognize and generate a set on simple objects should form the basis for complex object recognition.
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLfwj2X3BBTjXyaVNE2j7-wdEfqANKk3vbmRHcYorFZ1zOvMm9"  align="right">

There is a contrary view that in the nature you can barelly find abstrat geometrical shapes, like go in the forest and find me a triangle. Furthermore, neurons of a cat rised in the artificiall environments have distorted receptive fields, and are deficient in natural world. So, the appropiate way is to start with the natural images. However, we think that the brain converts the complex objects into the abstract to represent them more compactly, so the triangle IS in the forest, and it is in the human brain.  We are following the approach to start with simple shapes and to solve the basic questions that are unfortunatelly, rarely stated.

## The dot task
To simplify, consider one-dimesional discrete world of size $N$. The state is $x_i=0, i=1:N$ and the dot $x_j=1, j=some ~ number $.
How to encode the position of the dot to recognize:

1)if $j=50$

2)if $45<j<55$

3) if $ 50<j<N$

It is a binary recognition and the solution should follow the creationism principle.