# Deep Learning

Deep learning uses multi-layer neural networks to learn representations from
raw data.

## Neural Networks

A neural network is composed of layers of neurons. Each neuron computes a
weighted sum of its inputs, applies a non-linear activation function, and
passes the result to the next layer. The non-linearity is essential: without
it, stacked linear layers would collapse into a single linear transformation.

## Backpropagation

Backpropagation computes the gradient of the loss with respect to every
weight in the network using the chain rule, propagating errors backward from
the output layer to the input layer. Gradients are then used by an optimizer
such as SGD or Adam to update the weights.

## Activation Functions

- ReLU: fast, avoids vanishing gradients in deep networks, but can "die".
- Sigmoid: bounded 0-1, used for binary output, but saturates.
- Softmax: converts logits into a probability distribution, used for
  multi-class classification.

## Overfitting in Deep Learning

Large models memorize the training set. Regularization techniques include
dropout, weight decay (L2), early stopping, and data augmentation.

## Common Interview Questions

- What is the vanishing gradient problem and how is it addressed?
- Explain backpropagation in simple terms.
- Why do we need non-linear activation functions?
- What is dropout and why does it work?
- Difference between SGD, momentum, and Adam optimizers.
