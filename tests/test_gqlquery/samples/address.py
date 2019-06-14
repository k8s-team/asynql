from asynql import GQLModel


class Address(GQLModel):
    __one__ = 'address'
    __many__ = 'addresses'

    lat: float
    lon: float
    city: str
    line: str
