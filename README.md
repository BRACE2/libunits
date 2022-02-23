# libUnits

A simple unit library designed for embedding in other libraries.

## APIs

### Python API

### C API

```c
struct elle_UnitHandler metric_conversions = elle_metric_units();
```


### C++ API

```c++
elle::units::UnitHandler
```

## Accuracy

Each set of conversions carries an associated accuracy index. For example, in a set where length is represented in *inches*, an accuracy index of 10 indicates that all length conversions hold sufficient 


## Definitions



## References

SI Units: https://doi.org/10.6028/NIST.SP.330-2019

