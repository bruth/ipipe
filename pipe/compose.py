def compose(iterables, identity, merge, relative=False):
    """Composes a list of sorted `iterables` and yields one record at a
    time. During each iteration, all records that are next in line and
    have the same identity are merged right-to-left using the `merge`
    function.

    The `identity` takes a record and returns the key that the iterable
    has been sorted by. That is, if these are sequence of database rows
    with a primary key `id`, identity should return `id`.

    If `relative` is true, the first iterable will be treated as the _merge_
    target. Insteading of just yielding the composed record, the operation
    relative to the target will be returned. Possible operations include:

        0 - the record in target has been updated
        1 - the record is new and does not exist in target
       -1 - the record is in target, but not in any other source

    """

    iterables = [iter(itr) for itr in iterables]

    # Pending records by source index. Stored is a tuple of the identity
    # and record itself for the source
    pending = {}

    while True:
        changed = False
        lowmark = None

        for i, itr in enumerate(iterables):
            # Fetch from the pending cache if exists, otherwise proceed
            if i in pending:
                rid, record = pending.pop(i)
            else:
                try:
                    record = itr.next()
                    rid = identity(record)
                except StopIteration:
                    continue

            if lowmark is None or rid < pending[lowmark][0]:
                lowmark = i
            # If the identities match, merge the two records together
            elif rid == pending[lowmark][0]:
                changed = True
                out = merge(pending[lowmark][1], record)
                # Assume in-place merge
                if out is not None:
                    pending[lowmark][1] = out
                continue

            # Reached only when the record has not been changed
            pending[i] = [rid, record]

        if lowmark is None:
            raise StopIteration

        # Remove the lowmark from the pending
        rid, record = pending.pop(lowmark)

        # If `relative` is true, return the yield status of the record
        # as well. 0 denotes an update to the source record, -1 denotes
        # no other sources had the record, and 1 denotes a new record.
        if not relative:
            yield record
        elif lowmark == 0:
            if changed:
                yield 0, record
            else:
                yield -1, record
        else:
            yield 1, record
