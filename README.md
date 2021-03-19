# FIWARE ML as a Service POC
A simple Proof Of Concept for a FIWARE MLaaS.

This code is a ML algorithm that performs prediction from data stored into a FIWARE context broker (Stellio), and then store the prediction back into Stellio.

The consumer application could subscribe to change of the prediction data, and therefore be notified whenever a new prediction has been performed.

This code implements the following flow (the MLModel part).

![](./images/MLaaS-sequence.png)
