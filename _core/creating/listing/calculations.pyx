
def event_size(int h, int h2, int hs):
    #выводит текуще расположение у 
    cdef int p = int(h2-h2/(h/h2))

    if p*hs != 0:
        return int((h-h2)/p*hs)
    else:
        return 0

def update_size(int h, int h2):
        #выводит текуще каэфицент 
        try:
            return int(h2/(h/h2)), int(h2-h2/(h/h2))
        except ZeroDivisionError:
            return 0, h2