from asynql import GQLModel

from .address import Address


class Venue(GQLModel):
    __one__ = 'venue'
    __many__ = 'venues'

    uid: int
    title: str
    description: str
    address: Address
