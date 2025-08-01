

from abc import ABC
from itertools import combinations



# () means multiplication,Add,Sub
# {} curly ones means Exponent


def equals(obj1,obj2):
    if obj1 is None or obj2 is None:
        return obj1 is obj2
    if obj1.equaltype(obj2) == True:
     if isinstance(obj1,Constant) :
        return obj1.getnum() == obj2.getnum()
     if isinstance(obj1,Var) :
        return True
     if isinstance(obj1,Add) or isinstance(obj1,Sub) or isinstance(obj1,Mull):
         return equals(obj1.firstpart,obj2.firstpart) and equals(obj1.secendpart,obj2.secendpart)
     if isinstance(obj1,Expo):
         return equals(obj1.base,obj2.base) and equals(obj1.exponent,obj2.exponent)
    return False

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
           if ((x**i)/mark) <1e-5 :
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


class Expression(ABC):
    def __init__(self):
        self.integrationdepth = 0
    def integral(self):
        pass
    def getderivative(self):
        pass
    def evaluate(self):
        pass
    def tostring(self):
        pass
    def equaltype(self):
        pass
    def getdepth(self):
        return self._integration_depth
    def viable(self):
        self.integrationdepth+=1
        if self.integrationdepth > 1000:
            raise InvalidCombinationException("need to switch integration sides")
    def getname(self):
        return self.__class__._name__
    def defintegral(self,startpoint,endpoint):
        integral=self.integral()
        return integral.evaluate(endpoint) - integral.evaluate(startpoint)

class Constant(Expression): #any constant
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
    def __str__(self):
        return self.tostring()
    def add(self,num):
      if (isinstance(num,Constant)):
        return Constant(self.num+num.num)
      else:
          NotImplemented
    def integral(self):
        return Mull(Constant(self.num),Var())
    def equaltype(self,other):
        return isinstance(other,Constant)
    def getname(self):
        return "Constant"
class Var(Expression): #x
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
    def equaltype(self,other):
        return isinstance(other,Var)
    def getname(self):
        return "Var"
class Add(Expression):
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
        return f"({self.firstpart.tostring()} + {self.secendpart.tostring()})"
    def __str__(self):
        return self.tostring()
    def integral(self):
        return Add(self.firstpart.integral(),self.secendpart.integral())
    def equaltype(self,other):
        return isinstance(other,Add)
    def getname(self):
        return "Add"
class Mull(Expression):
    def __init__(self,firstpart,secendpart):
        self.firstpart=firstpart
        self.secendpart=secendpart
        self.integrationdepth=0
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
    def integral(self):#was tough. very tough.
            if type(self.firstpart) == Expo and type(self.secendpart) == Expo and type(self.firstpart.base) == Constant:
                raise InvalidCombinationException("please switch the order of the multiplication to x*A^x")
            if isinstance(self.firstpart, Constant):
                return Mull(self.firstpart, self.secendpart.integral())
            if isinstance(self.secendpart, Constant):
                return Mull(self.secendpart, self.firstpart.integral())
            if isinstance(self.firstpart, Expo) and isinstance(self.secendpart, Expo):
                if equals(self.firstpart.exponent, self.secendpart.exponent):
                    base = Mull(self.firstpart.base, self.secendpart.base)
                    simplified = Expo(base, self.firstpart.exponent)
                    return simplified.integral()
                if equals(self.firstpart.base, self.secendpart.base):
                    expo = Add(self.firstpart.exponent, self.secendpart.exponent)
                    simplified = Expo(self.firstpart.base, expo)
                    return simplified.integral()
            if (isinstance(self.firstpart, Expo) and
                    isinstance(self.firstpart.base, Var) and
                    isinstance(self.firstpart.exponent, Constant) and
                    isinstance(self.secendpart, Expo) and
                isinstance(self.secendpart.base, Constant) and
                    isinstance(self.secendpart.exponent, Var)):
                return self.integral_xn_ax(self.firstpart, self.secendpart)
            try:
                v_integral = self.secendpart.integral()
                part1 = Mull(self.firstpart, v_integral)
                part2 = Mull(self.firstpart.getderivative(), v_integral).integral()
                return Sub(part1, part2)
            except (RecursionError, InvalidCombinationException):
                if isinstance(self.secendpart, Expo) and isinstance(self.secendpart.base, Constant):
                    u_integral = self.firstpart.integral()
                    part1 = Mull(self.secendpart, u_integral)
                    part2 = Mull(self.secendpart.getderivative(), u_integral).integral()
                    return Sub(part1, part2)
                raise NotSupportedException("Integration failed - possibly unsupported pattern")
    def tostring(self):
        if self.firstpart is None or self.secendpart is None:
            return "Invalid Mull Expression"
        return f"({self.firstpart.tostring()}*{self.secendpart.tostring()})"
    def __str__(self):
        return self.tostring()
    def equaltype(self,other):
        return isinstance(other,Mull)
    def getname(self):
        return "Mull"
    def integral_xn_ax(self, xn_expr, ax_expr):
        n = xn_expr.exponent.getnum()
        a = ax_expr.base.getnum()
        ln_a = ln(a)
        if ln_a is None:
            raise InvalidCombinationException("Invalid base for logarithm")
        if n == 0:
            return Mull(ax_expr, Constant(1 / ln_a))
        else:
            term1 = Mull(xn_expr, ax_expr)
            term1 = Mull(term1, Constant(1 / ln_a))
            lower_power = Expo(Var(), Constant(n - 1))
            recursive_integral = self.integral_xn_ax(lower_power, ax_expr)
            term2 = Mull(Constant(n / ln_a), recursive_integral)
            return Sub(term1, term2)
class Sub(Expression):
    def __init__(self,firstpart,secendpart):
        self.firstpart=firstpart
        self.secendpart=secendpart
    def evaluate(self,x_value):
        if (type(x_value) == int or type(x_value) == float):
            return self.firstpart.evaluate(x_value) - self.secendpart.evaluate(x_value)
        else:
            raise InvalidCombinationException("evaluate doesnt accept non number types")
    def getderivative(self):
        return Sub(self.firstpart.getderivative(), self.secendpart.getderivative())
    def integral(self):
        return Sub(self.firstpart.integral(), self.secendpart.integral())
    def tostring(self):
        return f"{self.firstpart.tostring()}-{self.secendpart.tostring()}"
    def __str__(self):
        return self.tostring()
    def equaltype(self,other):
        return isinstance(other,Sub)
    def getname(self):
        return "Sub"
class Expo(Expression):
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
            return Mull(self, Constant(round(ln(self.base.getnum()),5)))

      if (isinstance(self.base,Var) and isinstance(self.exponent, Constant)) == True:
            return Mull(Expo(self.base,Constant(self.exponent.getnum()-1)),Constant(self.exponent.getnum()))

      raise NotSupportedException("we dont support x^x  integrals or derivatives|derivative error")
    def tostring(self):
         return  f"{self.base.tostring()}^{{{self.exponent.tostring()}}}"
    def __str__(self):
        return self.tostring()
    def integral(self):
        if type(self.base)==Constant and (type(self.exponent) == Var or type(self.exponent) == Add or type(self.exponent) == Sub): #replace the number with ln later
            return Mull(Mull(Expo(self.base,self.exponent),Constant(round(1/ln(self.base.getnum()),5))),self.exponent.getderivative())
        if type(self.base) == Constant and type(self.exponent) == Constant:
            return Mull(Expo(self.base,self.exponent),Var())
        if type(self.base) == Mull and type(self.exponent) == Var:
            if self.base.firstpart.equaltype(self.base.secendpart) and type( self.base.firstpart) == Constant:
                merger = self.base.firstpart.getnum() * self.base.secendpart.getnum()
                return Mull(Expo(Constant(merger), Var()), Constant(round(1 / ln(merger), 5)))
        if type(self.exponent) == Add and isinstance(self.base,Var):
            if self.exponent.firstpart.equaltype(self.exponent.secendpart) and type(self.exponent.firstpart) == Constant:
             merger=self.exponent.firstpart.getnum() + self.exponent.secendpart.getnum()
             return Expo(self.base,Constant(merger)).integral()
        if self.exponent.tostring() != "x":
            return Mull(Constant(1/(self.exponent.getnum()+1)),Expo(Var(),Constant(self.exponent.getnum()+1)))
        if isinstance(self.base, Constant) and isinstance(self.exponent, Var):
            return Mull(Expo(self.base,Var()),Constant(1 / ln(self.base.getnum())))
        raise NotSupportedException("we dont support x^x integrals or derivatives|integral error")
    def equaltype(self,other):
        return isinstance(other,Expo)
    def getname(self):
        return "Expo"
#format a^x*x works but only for x^a while a=1
#format x^a * b^x works for every a.
