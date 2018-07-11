The goal of the project is to experiment with neural encoding algorithms in order to find the way to learn connections without global optimization but with self-organization through local learning rules. 

In the usual neural networks, the main logic happens at the last layer. It dictates all other layers to change connections to reduce the error. An idea is that we need to spread (democratize) the choice for every individual neuron and give the decision to every cell independently. 
A single cell is seen as an agent that changes connections according to its inner dynamics.  

What type of dynamics is to determine in this project. 
To reduce possible options we build on top of previous ideas, mainly from computational neuroscience. 

Key features we intend to use:
1. Sparse distributed activation of a neural network. A motivation for this was written [here][1] (and many other sources). 
2. Competitive dynamics. An idea that neurons fight for the input to represent. That is how the neural specialization (formation of a receptive field should be achieved). There were many attempts but no one gave a completely satisfactory solution.
3. Neuron should receive top-down connections (beyond feedforward and lateral) and adjust weights accordingly. Information theory shows ([Tishby et al., 2017](https://arxiv.org/abs/1703.00810)) that more layers result in a better representation of an input. The neuron in the intermediate layer "knows" that its output will be used further and behaves differently compare to being alone. Backpropagation algorithm finds the optimal relation and makes the neural network process the input holistically. How to make this without global optimization is an open question. By asking it we as if go to 60ies, but now with the modern knowledge from the neuroscience and machine learning the second attempt might be successful.   

Guide for visitors:
1. Go to tasks and start with the [first][2]. It is simple but the solution is important for further use.
2. Try to solve the unsolved tasks. 
3. Read the essential papers in the file folder.
4. Contact us


  [1]: https://arxiv.org/abs/1503.07469
  [2]: https://osf.io/vxeah/

