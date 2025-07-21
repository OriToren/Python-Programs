
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
def ePower(x):
    sum=0
    mark=1
    try:
      for i in range(1000):
           sum+=((x**i) / mark)
           if i>=1:
               mark*=i+1
           if round(sum,5) == round(sum-((x**i)/mark),5):
               break
      if x>=0:
        return round(sum,5)
      else:
        return round(sum,5)
    except(OverflowError):
         if x>=0:
            return round(sum,5)
class ELNException(Exception):
    pass

class InvalidCombinationException(ELNException):
    def __init__(self,msg):
        super().__init__(msg)
class NotSupportedException(ELNException):
    def __init__(self,msg):
        super().__init__(msg)
class Constant: #any constant
    def __init__(self,num):
        self.num=num
    def getnum(self):
        return self.num
    def evaluate(self,anynum):
        return self.num
    def getderivative(self):
        return Constant(0)
    def tostring(self):
        return str(self.num)
    def add(self,num):
      if (isinstance(num,Constant)):
        return Constant(self.num+num.num)
      else:
          NotImplemented
    def integral(self):
        return Mull(Constant(self.num),Var())

class Var: #x
    def evaluate(self,num):
        return num
    def getderivative(self):
        return Constant(1)
    def tostring(self):
        return "x"
    def integral(self):
        integral=Mull(Constant(1/2),Expo(Var(),Constant(2)))
        return integral
    def getnum(self):
        return 0
class Function:
    def __init__(self,base,fx,gx):
         self.base=base
         self.fx=fx
         self.gx=gx
    def getbase(self):
        return self.base.tostring()
    def getexpo(self):
        return self.expo.tostring()
    def getfx(self):
        return self.gx.tostring()
    def tostring(self):
        return f"{self.base.tostring()}^({self.fx.tostring()}) * {self.gx.tostring()}"
    def __str__(self):
        return self.tostring()
class Add:
    def __init__(self,firstpart,secendpart):
        self.firstpart=firstpart
        self.secendpart=secendpart
    def evaluate(self,x_value):
        if (type(x_value) == int or type(x_value) == float):
         return self.firstpart.evaluate(x_value) + self.secendpart.evaluate(x_value)
        else:
            raise InvalidCombinationException("evaluate doesnt accept non number types")
    def getderivative(self):
        return Add(self.firstpart.getderivative(),self.secendpart.getderivative())
    def tostring(self):
        return f"{self.firstpart.tostring()} + {self.secendpart.tostring()}"
    def __str__(self):
        return self.tostring()
    def integral(self):
        return Add(self.firstpart.integral(),self.secendpart.integral())
class Mull:
    def __init__(self,firstpart,secendpart):
        self.firstpart=firstpart
        self.secendpart=secendpart
    def evaluate(self,x_value):

            if (type(x_value) == int or type(x_value) == float):
                return self.firstpart.evaluate(x_value) * self.secendpart.evaluate(x_value)
            else:
                raise InvalidCombinationException("evaluate doesnt accept non number types")
    def getderivative(self):
        if (isinstance(self.firstpart,Constant) and isinstance(self.secendpart,Constant)) == True: #edgecases
            return Constant(0)
        if (isinstance(self.firstpart,Constant) and isinstance(self.secendpart,Var)) == True:
            return Constant(self.firstpart.getnum())
        if (isinstance(self.firstpart,Var) and isinstance(self.secendpart,Constant)) == True:
            return Constant(self.secendpart.getnum())
        return Add(Mull(self.firstpart.getderivative(), self.secendpart),Mull(self.firstpart, self.secendpart.getderivative()))
 #   def integral(self):
#        return Add(Mull(self.firstpart,self.secendpart.integral()),integral(Mull(self.firstpart.getderivative(),self.secendpart.integral()))) #workon this tomorow

    def tostring(self):
        return f"{self.firstpart.tostring()}*{self.secendpart.tostring()}"
    def __str__(self):
        return self.tostring()
class Expo:
    def __init__(self,base,exponent):
        self.base=base
        self.exponent=exponent
    def evaluate(self,x_value):
        if (type(x_value) == int or type(x_value) == float):
            return self.base.evaluate(x_value) ** self.exponent.evaluate(x_value)
        else:
            raise InvalidCombinationException("evaluate doesnt accept non number types")
    def getderivative(self):
        if (isinstance(self.base,Constant) and isinstance(self.exponent,Constant)) == True: #edgecases
            return Constant(0)
        if (isinstance(self.base, Constant) and isinstance(self.exponent, Var)) == True:
            return Mull(self, Constant(ln(self.base.getnum())))
        if (isinstance(self.base,Var) and isinstance(self.exponent, Constant)) == True:
            return Mull(Expo(self.base,Constant(self.exponent.getnum()-1)),Constant(self.exponent.getnum()))
    def tostring(self):
        return  f"{self.base.tostring()}^({self.exponent.tostring()})"
    def __str__(self):
        return self.tostring()
    def integral(self):
        if type(self.base)==Constant and type(self.exponent) == Var: #replace the number with ln later
            return Mull(Expo(self.base,self.exponent),Constant(ln(self.base.getnum())))
        if type(self.base) == Constant and type(self.exponent) == Constant:
            return Mull(Expo(self.base,self.exponent),Var())
        if self.exponent.tostring() != "x":
            return Mull(Constant(1/(self.exponent.getnum()+1)),Expo(Var(),Constant(self.exponent.getnum()+1)))
        try:
         raise NotSupportedException("we dont support x^x integrals or derivatives")
        except NotSupportedException as e:
             print(e)
             return
#print(Add(Constant(3),Mull(Constant(3),Var())))
#print(Mull(Consant(3),Var()))
func=Mull(Expo(Constant(3),Var()),Var())
print(func.getderivative())
