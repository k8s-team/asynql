[![GraphQL logo](https://raw.githubusercontent.com/k8s-team/asynql/master/logo.png)](https://github.com/k8s-team/asynql)

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
