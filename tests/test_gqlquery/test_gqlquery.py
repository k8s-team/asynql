from .samples import Concert, Venue, Address


def test_one_field():
    query = Concert.many(Concert.title).to_gql()
    assert query == "{ concerts { title } }"


def test_two_fields():
    query = Concert.many(Concert.title, Concert.uid).to_gql()
    assert query == "{ concerts { title uid } }"


def test_inner_gql_field():
    query = Concert.many(Concert.venue_main).to_gql()
    assert query == "{ concerts { venue_main } }"


def test_many_inner_gql_field_expand():
    query = Concert.many(
        Concert.title,
        Concert.venue_main.q(
            Venue.title
        ),
        Concert.venue_reserved.q(
            Venue.title
        )
    ).to_gql()
    assert query == "{ concerts " \
                    "{ title venue_main { title } " \
                    "venue_reserved { title } } }"


def test_one_inner_gql_field_expand():
    query = Concert.one(
        Concert.title,
        Concert.venue_main.q(
            Venue.title
        ),
        Concert.venue_reserved.q(
            Venue.title
        ),
        uid=123
    ).to_gql()
    assert query == "{ concert(uid: 123) " \
                    "{ title venue_main { title } " \
                    "venue_reserved { title } } }"


def test_complex_query():
    query = Concert.many(
        Concert.title,
        Concert.venue_main.q(
            Venue.title,
            Venue.address.q(
                Address.line
            )
        )
    ).to_gql()
    assert query == "{ concerts " \
                    "{ title venue_main { title address { line } } } }"
