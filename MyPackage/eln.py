import quadratic
class exponentException(Exception):
    pass
class InvalidFormatException(exponentException):
    def __init__(self):
        super().__init__("Wrong format for exponent function")

def ePower(x):
    # using ePower(ln(x)) == x breaks for some reason even tho for the same x ePower(x) works #fixed.
    sum=0
    mark=1
    try:
      for i in range(1000):
           sum+=((x**i) / mark)
           if i>=1:
               mark*=i+1
      if x>=0:
        return round(sum,5)
      else:
        return round(sum,5)
    except(OverflowError):
         if x>=0:
            return round(sum,5)
def ln(x):
    if x<0:
        return None
    sum=0
    # we will use a diffrent taylor series expansion from Math2.org .
    # starts to diverge around x=400 but still remains fairly close until close to a 1000
    for i in range(1,101):
        if x==ePower(i):
            return i
    try:
        if x>0.5:
         for i in range(1,1000):
             sum=sum+((x-1)**i/x**i)/i
         return round(sum,5)
    except(OverflowError):
        return round(sum,5)
    # we will use the classic taylor series expansion for ln(x)
    for i in range(1,1000):
        sum=sum+((x-1)**i / i )*(-1)**(i+1)
    return round(sum,5)


def lnList(items):
    for item in range(len(items)):
        if isinstance(items[item],float,int) and items[item] > 0:
         if ln(items[item]) != None:
          items[item]=ln(items[item])
         else:
            return False
        else:
            return False
    return items
"""
 if isinstance(a,tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            fx = temp[1]
            gx = temp[2]
    try:
        if _check_eln(a, fx, gx) == False:
            raise InvalidFormatException
    except InvalidFormatException as e:
        print(e)
        return
"""
def _check_eln(a,fx,gx):
    if (type(a) != float and type(a) != int) or (type(fx) != tuple) or (type(gx) != tuple and gx != 1):
        return False
    return True
def getFunc(number:float,exponent:tuple,times_this:tuple):
    return (number,exponent,times_this)
def Roots(a:float,fx:tuple=None,gx:tuple=None):
    if isinstance(a, tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            fx = temp[1]
            gx = temp[2]
    try:
        if _check_eln(a, fx, gx) == False:
            raise InvalidFormatException
    except InvalidFormatException as e:
        print(e)
        return
    return quadratic.Roots(gx) #a^f(x) cant be zero
def Derivative(a:float,fx:float=None,gx:tuple or float = None):
    if isinstance(a, tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            fx = temp[1]
            gx = temp[2]
    try:
        if _check_eln(a, fx, gx) == False:
            raise InvalidFormatException
    except InvalidFormatException as e:
        print(e)
        return
    if gx==1 or gx==(0,0,0):
        return (a,fx,quadratic.mullFunc(quadratic.Derivative(fx),ln(a)))
