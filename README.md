# Continous_and_Discrete_Dynamic_Nonlinear_Flow_Algorithm
A modified version of flow algorithm for continuous and discrete dynamic nonlimear flows

* This is a dynamic non-linear flow algorithm based on dinitz flow algorithm.
* The Algorithm has been extended by two feathres: 1) Continous flow, 2) Discrete flow
* Furthermore, the algorithm is modified to provide two type of outputs: 1) Residual graph, 2) minmax graph.
* The residual graph is suitable for continous flow and the minmax graph is suitable for discrete flow, but both can be generated at the same time
* The residual graph's lowest value indicate the bottleneck is higher, the mixmax graph shows the persistency of the botttlneck.
* If the variance in minmax graph is small, it means that there was a persistent bottleneck.

