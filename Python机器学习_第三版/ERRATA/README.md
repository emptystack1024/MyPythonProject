# Current Errata

## Chapter 3

**Page 66**

The doc strings of the LogisticRegressionGD classifier reference "Mean squared error loss" -- this is a copy-paste error and should be "Log loss".

## Chapter 11

**Page 341**

Add bias unit to the net input.

**Page 361**

$$\frac{\partial}{\partial w_{j, l}^{(l)}}=L(\boldsymbol{W}, \boldsymbol{b})$$ 

should be 

$$\frac{\partial L}{\partial w_{j, l}^{(l)}}$$ 

## Chapter 12

**Page 380**

We use `TensorDataset` even though we defined the custom `JointDataset`

## Chapter 13

**Page 431**

When using Torchmetrics 0.8.0 or newer, the following lines

```python
self.train_acc = Accuracy()
self.valid_acc = Accuracy()
self.test_acc = Accuracy()
```

need to be changed to

```python
self.train_acc = Accuracy(task="multiclass", num_classes=10)
self.valid_acc = Accuracy(task="multiclass", num_classes=10)
self.test_acc = Accuracy(task="multiclass", num_classes=10)
```

## Chapter 15



**Page 530**

The line `from torch.utils.data import Dataset` appears twice.



---



For books printed before 16 Nov 2022, please see the [Old Errata](old-errata).



