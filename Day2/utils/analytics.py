def total(m, s, e):
    return (int(m)+int(s)+int(e))/3

def grade(t):
    if t >= 85: return "A"
    elif t >= 70: return "B"
    elif t >= 50: return "C"
    else: return "F"