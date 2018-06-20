def get_prime(begin, end):
    for num in range(begin, end):
        if num == 1:
            continue
        
        elif num % 2 == 0: #even number
            if num == 2:
                yield num
            else:
                continue
            
        else:
            for candidate in range(2, num):
                if num % candidate == 0:
                    break
            if candidate == num - 1:
                yield num
            else:
                continue
