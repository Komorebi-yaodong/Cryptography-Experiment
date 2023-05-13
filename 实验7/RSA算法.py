def expand_gcd(a, b):
    def sub_gcd(a,b):
        if b == 0:
            return 1,0,a
        else:
            x_, y_ , gcd = sub_gcd(b, a % b)
            x = y_
            y = x_ - (a // b) * y_
            return x,y,gcd
    x,y,gcd = sub_gcd(a,b)
    if x < 0:
        x = x%b
        y = (gcd-x*a)//b
    return x,y,gcd


