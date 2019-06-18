from asynql import GQLModel

from .venue import Venue


class Concert(GQLModel):
    __one__ = 'concert'
    __many__ = 'concerts'

    uid: int
    title: str
    url: str
    venue_main: Venue
    venue_reserved: Venue
