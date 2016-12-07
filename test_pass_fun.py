
def test(a,b):
    print a+b
    

def wraper(fun,*args):
    print 'Hello'
    fun(*args)

test(2, 3)

wraper(test,5,4)