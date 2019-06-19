[![GraphQL logo](https://raw.githubusercontent.com/k8s-team/asynql/master/logo.png)](https://github.com/k8s-team/asynql)

-----

[![Build Status](https://travis-ci.org/k8s-team/asynql.svg?branch=master)](https://travis-ci.org/k8s-team/asynql) 
[![Coverage Status](https://coveralls.io/repos/github/k8s-team/asynql/badge.svg?branch=master)](https://coveralls.io/github/k8s-team/asynql?branch=master)
[![Documentation Status](https://readthedocs.org/projects/asynql/badge/?version=latest)](https://asynql.readthedocs.io/en/latest/?badge=latest) 
[![Python Version](https://img.shields.io/pypi/pyversions/asynql.svg)](https://pypi.org/project/asynql/) 

-----

# asynql


Asyncio `GraphQL` client

## Usage

```python
from asynql import GQLModel

class Address(GQLModel):
    __one__ = 'address'
    __many__ = 'addresses'

    lat: float
    lon: float
    city: str
    line: str
```

We need `__one__` and `__many__` to be specified to customize query for one item or for many items.
