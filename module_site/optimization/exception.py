class BinaryChromosomeBoundaryError(Exception):
    def __init__(self, bound_info):
        check = True
        min_value, max_value, num_digit = bound_info
        if min_value < 0 or max_value >= pow(2, num_digit):
            check = False
            print('min value have to be positive')
        elif max_value >= pow(2, num_digit):
            check = False
            print('max value have to be smaller than num_digit')
        else:
            check = True

