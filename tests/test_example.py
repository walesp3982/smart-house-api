def sum(a, b):
    return a + b 

def test_sum():
    a = 2
    b = 2
    c = sum(a,b)
    assert 4 == c