def ladnerfischer(rank, size):
    calls = []
    ranks = list(range(0, size))
    ladnerfischer_work(0, rank, 0, size, ranks, calls)
    return calls
    
def ladnerfischer_work(level, rank, begin, size, ranks, calls):

    # only works for powers of two
    new_size = int(size / 2)
    
    if size == 2:
        if rank % 2 == 1:
            calls.insert( 0, ('receive', ranks[rank - 1]))
        else:
            calls.insert(0, ('send', ranks[rank + 1]))
        return
    
    if level == 1:
        # last send from each
        position_inside = rank
        # is the rank inside the recursive call?
        # order: receive from previous rank, recursive call, send to next rank (except last one)
        if position_inside % 2 == 1:
            
            if position_inside < size - 1:
                calls.insert(0, ('send', ranks[position_inside + 1]))
            new_ranks = [ ranks[x] for x in range(begin+1, size, 2)]
            # new rank is the idx across odd ranks
            new_rank = int((rank - 1) / 2)
            ladnerfischer_work(0, new_rank, begin + 1, new_size, new_ranks, calls)
            calls.insert(0, ('receive', ranks[position_inside - 1]))
        # rank does not participate in the recursive call
        # order: send to next rank, receive from the previous one (except the first one)
        else:
            if position_inside > 0:
                calls.insert(0, ('receive', ranks[position_inside - 1]))
            calls.insert(0, ('send', ranks[position_inside + 1]))
    else:
        # next with level 1
        if rank < new_size:
            new_ranks = ranks[0:new_size]
            new_rank = rank

            # broadcast from last rank of left side to others
            if new_rank == len(new_ranks) - 1:
                calls.insert(0, ('broadcast', begin+new_size, new_size))
            ladnerfischer_work(1, new_rank, begin, new_size, new_ranks, calls)
        else:
            new_ranks = ranks[new_size:size]
            new_rank = rank % new_size
            # propagate results from the end of other half
            calls.insert(0, ('broadcast_recv', begin + new_size - 1))
            ladnerfischer_work(0, new_rank, begin + new_size, new_size, new_ranks, calls)

assert ladnerfischer(0, 2) == [('send', 1)]
assert ladnerfischer(1, 2) == [('receive', 0)]

assert ladnerfischer(0, 4) == [('send', 1)]
assert ladnerfischer(1, 4) == [('receive', 0), ('broadcast', 2, 2)]
assert ladnerfischer(2, 4) == [('send', 3), ('broadcast_recv', 1)]
assert ladnerfischer(3, 4) == [('receive', 2), ('broadcast_recv', 1)]

assert ladnerfischer(0, 8) == [('send', 1)]
assert ladnerfischer(1, 8) == [('receive', 0), ('send', 3), ('send', 2)]
assert ladnerfischer(2, 8) == [('send', 3), ('receive', 1)]
assert ladnerfischer(3, 8) == [('receive', 2), ('receive', 1), ('broadcast', 4, 4)]
assert ladnerfischer(4, 8) == [('send', 5), ('broadcast_recv', 3)]
assert ladnerfischer(5, 8) == [('receive', 4), ('broadcast', 6, 2), ('broadcast_recv', 3)]
assert ladnerfischer(6, 8) == [('send', 7), ('broadcast_recv', 5), ('broadcast_recv', 3)]
assert ladnerfischer(7, 8) == [('receive', 6), ('broadcast_recv', 5), ('broadcast_recv', 3)]
