def filterValidLinks(array):
    def filter_func(item):
        if len(item) and item.startswith('http'):
            return True
        else:
            return False
    return filter(filter_func, array)
