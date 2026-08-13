# Machine Learning Fundamentals

Machine learning is the study of computer algorithms that improve automatically
through experience.

## Supervised Learning

In supervised learning the training data contains labeled examples: an input
and the correct output. The model learns a mapping from inputs to outputs and
generalizes to unseen data. Common tasks are classification (predicting a
category) and regression (predicting a continuous value).

## Unsupervised Learning

In unsupervised learning the data has no labels. The goal is to find structure
in the data. Common tasks are clustering (grouping similar points) and
dimensionality reduction (compressing features while keeping structure).

## Bias and Variance

Bias is the error introduced by approximating a real problem with a too-simple
model. Variance is the error introduced by a model that is too sensitive to
small fluctuations in the training data. High bias causes underfitting; high
variance causes overfitting.

## Cross-Validation

Cross-validation splits the data into folds and trains the model on all but
one fold, evaluating on the held-out fold, repeated for every fold. This gives
a more reliable estimate of generalization than a single train/test split.

## Common Interview Questions

- Explain the difference between supervised and unsupervised learning.
- What is overfitting and how do you prevent it?
- What is the bias-variance tradeoff?
- Why do we split data into train, validation, and test sets?
- What is cross-validation and when would you use it?
