

from abc import ABC

import random


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

def ln(x, terms=50):
    if x <= 0:
        raise ValueError("ln undefined for non-positive x")
    for i in range(0,100):
        if x == ePower(i):
            return i
    k = 0
    while x > 1.5:
        x /= 2
        k += 1
    while x < 0.5:
        x *= 2
        k -= 1
    z = x - 1
    total = 0.0
    sign = 1
    for n in range(1, terms + 1):
        term = sign * (z ** n) / n
        total += term
        sign *= -1
    LN2 = 0.6931471805599453 #ln2
    return total + k * LN2
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
class InvalidNumException(ELNException):
    def __init__(self,msg):
        super().__init__(msg)


class Expression(ABC):
    def __init__(self):
        pass
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
    def getname(self):
        return self.__class__._name__
    def defintegral(self,startpoint,endpoint):
        integral=self.integral()
        return integral.evaluate(endpoint) - integral.evaluate(startpoint)
    def simplify(self):
        pass
    def fully_simplify(self):
     while not self.simple:
        self=self.simplify()
     return self
    def isodd(self):
        if self.defintegral(-1,1) == 0 and self.defintegral(-2.654346,2.654346)==0:
            return True
        return False
    def iseven(self):
        if 2*self.defintegral(0,1)==self.defintegral(-1,1) and 2*self.defintegral(0,2.654346)==self.defintegral(-2.654346,2.654346):
            return True
        return False
    def y_inter(self):
        return self.evaluate(0)
    def tan_line(self,xpoint):
        derivative=self.getderivative()
        tang_m=derivative.evaluate(xpoint)
        ypoint=self.evaluate(xpoint)
        firstpart=Mull(tang_m,Sub(x,xpoint))
        return Add(firstpart.simplify(),ypoint).simplify()
    def isprimitive(self):
        if isinstance(self,(Var,Constant)):
            return True
        return False
    def info(self):
       try:
        return {"Function":self,
                "Function Derivative":self.getderivative(),
                "Function Integral":self.integral(),
                "y intercept":self.y_inter()}
       except AttributeError as e:
          NotImplemented
    def printinfo(self):
      try:
       dic=self.info()
       for key,value in dic.items():
            print(key,value)
      except AttributeError as e:
          NotImplemented
    def __add__(self, other): #for helping writings
            return Add(self, other)
    def __radd__(self, other):
            return Add(other, self)
    def __sub__(self, other):
            return Sub(self, other)
    def __rsub__(self, other):
            return Sub(other, self)
    def __mul__(self, other):
            return Mull(self, other)
    def __rmul__(self, other):
            return Mull(other, self)
    def __truediv__(self, other):
            return Div(self, other)
    def __rtruediv__(self, other):
            return Div(other, self)
    def __pow__(self, other):
            return Expo(self, other)
    def __rpow__(self, other):
            return Expo(other, self)
class Constant(Expression): #any constant
    def __init__(self,num):
        self.num=num
        self.simple=True
    def getnum(self):
        return self.num
    def evaluate(self,anynum):
        return self.num
    def getderivative(self):
        return Constant(0)
    def tostring(self):
        if equals(Constant(e),self):
            return "e"
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
    def simplify(self):
        return self
class Var(Expression):#x
    def __init__(self):
        self.simple=True
    def evaluate(self,num):
        return num
    def getderivative(self):
        return Constant(1)
    def tostring(self):
        return "x"
    def __str__(self):
        return Var().tostring()
    def integral(self):
        integral=Mull(Constant(1/2),Expo(Var(),Constant(2)))
        return integral
    def getnum(self):
        return 0
    def equaltype(self,other):
        return isinstance(other,Var)
    def getname(self):
        return "Var"
    def simplify(self):
        return self
class Add(Expression):
    def __init__(self,firstpart,secendpart,simple=None):
        self.firstpart=firstpart
        self.secendpart=secendpart
        self.simple=simple
        if isinstance(self.firstpart,(int,float)):
            self.firstpart=Constant(firstpart)
        if isinstance(self.secendpart,(int,float)):
            self.secendpart=Constant(secendpart)
        if self.simple==None:
         self.simple=False
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
    def simplify(self):
       try:
        if equals(self.firstpart,self.secendpart):
            return Mull(2,self.firstpart)
        if equals(self.firstpart,Constant(0)):
            return self.secendpart
        if equals(self.secendpart,Constant(0)):
            return self.firstpart
        if self.firstpart.simple==True and self.secendpart.simple==True  or (self.getname()=="Ln" and self.simple==True):
          if (isinstance(self.firstpart, Mull) and isinstance(self.secendpart, Mull)):
                fp1 = self.firstpart.firstpart
                fp2 = self.firstpart.secendpart
                sp1 = self.secendpart.firstpart
                sp2 = self.secendpart.secendpart
                if equals(fp1, sp1) and isinstance(fp1, Var) and fp2.equaltype(sp2) and isinstance(fp2, Constant):
                    return Mull(Constant(fp2.getnum() + sp2.getnum()), Var)
                if equals(fp1, sp2) and isinstance(fp1, Var) and fp2.equaltype(sp1) and isinstance(fp2, Constant):
                    return Mull(Constant(fp2.getnum() + sp1.getnum()), Var())
                if fp1.equaltype(sp1) and isinstance(fp1, Constant) and fp2.equaltype(sp2) and isinstance(fp2, Var):
                    return Mull(Constant(fp1.getnum() + sp1.getnum()), Var())
                if fp1.equaltype(sp2) and isinstance(fp1, Constant) and fp2.equaltype(sp1) and isinstance(fp2, Var):
                    return Mull(Constant(fp1.getnum() + sp2.getnum()), Var())
          if isinstance(self.firstpart,Mull):
              if (isinstance(self.firstpart.firstpart,Constant) and isinstance(self.firstpart.secendpart,Var)) and equals(self.secendpart,Var()):
                  return Mull(Constant(self.firstpart.firstpart.getnum()+1),Var())
              if (isinstance(self.firstpart.secendpart,Constant) and isinstance(self.firstpart.firstpart,Var)) and equals(self.secendpart,Var()):
                  return Mull(Constant(self.firstpart.secendpart.getnum()+1),Var())
          if isinstance(self.secendpart, Mull):
              if  (isinstance(self.secendpart.firstpart,Constant) and isinstance(self.secendpart.secendpart,Var)) and equals(self.firstpart,Var()):
                  return Mull(Constant(self.secendpart.firstpart.getnum()+1),Var())
              if (isinstance(self.secendpart.secendpart, Constant) and isinstance(self.secendpart.firstpart,Var)) and equals(self.firstpart, Var()):
                  return Mull(Constant(self.secendpart.secendpart.getnum()+1),Var())
          if not(isinstance(self.firstpart,(Var,Constant)) or isinstance(self.secendpart,(Var,Constant))):
            self.simple=True
            return self
          elif isinstance(self.firstpart, (Var, Constant)) and isinstance(self.secendpart,(Sub, Add)) and (isinstance(self.secendpart.firstpart,(Var, Constant)) and isinstance(self.secendpart.secendpart,(Var, Constant))):
                fp = self.secendpart.firstpart
                sp = self.secendpart.secendpart
                if fp.equaltype(self.firstpart) and not isinstance(self.secendpart,(Expo,Mull)):
                    if not self.secendpart.equaltype(Sub(1,1)):
                     return Add(Add(fp, self.firstpart).simplify(),sp)
                    else:
                     return Add(Sub(fp,self.firstpart).simplify(),sp)
                if sp.equaltype(self.firstpart):
                    if not self.secendpart.equaltype(Sub(1,1)):
                     return Add(Add(sp,self.firstpart).simplify(),fp)
                    return Add(Sub(sp,self.firstpart).simplify(),fp)
          elif not isinstance(self.firstpart,(Var,Constant)) and not isinstance(self.firstpart,(Expo,Mull)):
            fp = self.firstpart.firstpart
            sp = self.firstpart.secendpart
            if fp.equaltype(self.secendpart) and not isinstance(self.secendpart,(Expo,Mull)):
                if not self.firstpart.equaltype(Sub(-1,1)):
                 return Add(Add(fp,self.secendpart).simplify(),sp)
                else:
                 return Add(Sub(fp,self.secendpart).simplify(),sp)
            if sp.equaltype(self.secendpart) and not isinstance(self.firstpart,(Expo,Mull)) :
                if not self.firstpart.equaltype(Sub(-1,1)):
                 return Add(Add(sp,self.secendpart).simplify(),fp)
                else:
                 return Add(Sub(sp,self.secendpart).simplify(),fp)
          elif isinstance(self.firstpart, (Mull, Expo,Sub,Add)) or isinstance(self.secendpart, (Mull, Expo,Sub,Add)):
              self.simple=True
              return self
        if not (isinstance(self.firstpart, (Var, Constant)) and isinstance(self.secendpart, (Var, Constant))):
            return Add(self.firstpart.simplify(),self.secendpart.simplify()).simplify()
        if isinstance(self.secendpart,Constant) and isinstance(self.firstpart,Constant):
            if self.firstpart.getnum()==-self.secendpart.getnum():
                return Constant(0)
            else:
             return Constant(self.firstpart.getnum()+self.secendpart.getnum())
        if isinstance(self.firstpart,Constant) and equals(self.firstpart,Constant(0)):
            return self.secendpart
        if isinstance(self.secendpart,Constant) and equals(self.secendpart,Constant(0)):
            return self.firstpart
        if isinstance(self.secendpart,Var) and isinstance(self.firstpart,Var):
            return Mull(Constant(2),Var())
        if equals(self.firstpart,Constant(0)):
            return self.secendpart
        if equals(self.secendpart,Constant(0)):
            return self.firstpart
        if isinstance(self.firstpart,(Add,Sub)) or isinstance(self.secendpart,(Add,Sub)) and self.simple==False:
           if isinstance(self.firstpart, (Var,Constant)):
               return Add(self.firstpart,self.secendpart.simplify()).simplify()
           else:
               return Add(self.firstpart.simplify(),self.secendpart).simplify()
        self.simple=True
        return self
       except RecursionError as e:
        return self
class Mull(Expression):
    def __init__(self,firstpart,secendpart,simple=None):
        self.firstpart=firstpart
        self.secendpart=secendpart
        self.simple=simple
        if isinstance(self.firstpart,(int,float)):
            self.firstpart=Constant(firstpart)
        if isinstance(self.secendpart,(int,float)):
            self.secendpart=Constant(secendpart)
        if self.simple==None:
         self.simple=False
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
                raise NotSupportedException("Integration failed,possibly not supported")
    def tostring(self):
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
    def simplify(self):
       try:
        if isinstance(self.firstpart,Var) and isinstance(self.secendpart,Var):
            return Expo(Var(),Constant(2))
        if isinstance(self.firstpart,Expo) and isinstance(self.secendpart,Expo) and equals(self.firstpart.base,self.secendpart.base):
            return Expo(self.firstpart.base,Add(self.firstpart.exponent,self.secendpart.exponent))
        if isinstance(self.firstpart,Expo) and isinstance(self.secendpart,Expo) and equals(self.firstpart.exponent,self.secendpart.exponent):
            return Expo(Mull(self.firstpart.base,self.secendpart.base),self.firstpart.exponent)
        if (isinstance(self.firstpart, Constant) and self.firstpart.getnum() == 0) or  (isinstance(self.secendpart, Constant) and self.secendpart.getnum() == 0):
            return Constant(0)
        if equals(self.firstpart,Constant(1)):
            return self.secendpart
        if equals(self.secendpart,Constant(1)):
            return self.firstpart
        if isinstance(self.firstpart,Constant) and isinstance(self.secendpart,Constant):
            return Constant(self.firstpart.getnum()*self.secendpart.getnum())
        if isinstance(self.firstpart,Mull) and isinstance(self.secendpart,Mull) and self.firstpart.simple and self.secendpart.simple:
            if (isinstance(self.firstpart.firstpart,Constant) and isinstance(self.firstpart.secendpart,Var)) or \
                (isinstance(self.firstpart.firstpart,Var) and isinstance(self.firstpart.secendpart,Constant)) and (isinstance(self.secendpart.firstpart,Constant) and isinstance(self.secendpart.secendpart,Var)) or \
                (isinstance(self.secendpart.firstpart,Var) and isinstance(self.secendpart.secendpart,Constant)):
                fp1=self.firstpart.firstpart
                fp2=self.firstpart.secendpart
                sp1=self.secendpart.firstpart
                sp2=self.secendpart.secendpart
                if isinstance(fp1,Constant) and fp1.equaltype(sp1):
                    return Mull(fp1.getnum()*sp1.getnum(),Expo(Var(),2))
                if isinstance(fp1,Constant) and fp1.equaltype(sp2):
                    return Mull(fp1.getnum()*sp2.getnum(),Expo(Var(),2))
                if isinstance(fp2,Constant) and fp2.equaltype(sp1):
                    return Mull(fp2.getnum()*sp1.getnum(),Expo(Var(),2))
                if isinstance(fp2,Constant) and fp2.equaltype(sp2):
                    return Mull(fp2.getnum()*sp2.getnum(),Expo(Var(),2))

        if (isinstance(self.firstpart,Constant) and isinstance(self.secendpart,Expo) and (isinstance(self.secendpart.base,Constant))):
            return Expo(self.secendpart.base,Add(self.secendpart.exponent,ln(self.firstpart.getnum())/ln(self.secendpart.base.getnum())))
        if (isinstance(self.secendpart,Constant) and isinstance(self.firstpart,Expo) and (isinstance(self.firstpart.base,Constant))):
            return Expo(self.firstpart.base,Add(self.firstpart.exponent,ln(self.secendpart.getnum())/ln(self.firstpart.base.getnum())))
        if (isinstance(self.firstpart,Constant) and isinstance(self.secendpart,(Sub,Add))) or (isinstance(self.firstpart,(Add,Sub)) and isinstance(self.secendpart,Constant)):
            if isinstance(self.firstpart,Constant) and isinstance(self.secendpart,Sub) and isinstance(self.secendpart.secendpart,Constant):
                return Add(Mull(self.firstpart, self.secendpart.firstpart),Mull(self.firstpart,-1*self.secendpart.secendpart.getnum()))
            if isinstance(self.firstpart, Constant) and isinstance(self.secendpart, Sub):
                return Add(Mull(self.firstpart, self.secendpart.firstpart),Mull(self.firstpart, Sub(0,self.secendpart.secendpart)))
            if isinstance(self.firstpart,Constant) :
                return Add(Mull(self.firstpart,self.secendpart.firstpart),Mull(self.firstpart,self.secendpart.secendpart))
            if  isinstance(self.secendpart,Constant) and isinstance(self.firstpart,Sub) and isinstance(self.firstpart.secendpart,Constant):
                return Add(Mull(self.secendpart,self.firstpart.firstpart),Mull(self.secendpart,-1*self.firstpart.secendpart.getnum()))
            if isinstance(self.secendpart, Constant) and isinstance(self.firstpart, Sub) and isinstance(self.firstpart.secendpart, Constant):
                return Add(Mull(self.secendpart, self.firstpart.firstpart),Mull(self.secendpart, Sub(0, self.firstpart.secendpart)))
            if  isinstance(self.secendpart, Constant):
                return Add(Mull(self.secendpart, self.firstpart.firstpart),Mull(self.secendpart,self.firstpart.secendpart))
        if (isinstance(self.firstpart,(Expo,Mull,Add,Sub)) or isinstance(self.secendpart,(Expo,Mull,Add,Sub))) and self.simple==False:
            if (isinstance(self.firstpart,(Expo,Mull,Add,Sub))):
                self.firstpart=self.firstpart.simplify()
            if (isinstance(self.secendpart,(Expo,Mull,Add,Sub))):
                self.secendpart=self.secendpart.simplify()
            return Mull(self.firstpart,self.secendpart)
        self.simple=True
        return self
       except RecursionError as e:
           return self
class Sub(Expression):
    def __init__(self,firstpart,secendpart,simple=None):
        self.firstpart=firstpart
        self.secendpart=secendpart
        self.simple=simple
        if isinstance(self.firstpart,(int,float)):
            self.firstpart=Constant(firstpart)
        if isinstance(self.secendpart,(int,float)):
            self.secendpart=Constant(secendpart)
        if self.simple==None:
         self.simple=False
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
        return f"({self.firstpart.tostring()}-{self.secendpart.tostring()})"
    def __str__(self):
        return self.tostring()
    def equaltype(self,other):
        return isinstance(other,Sub)
    def getname(self):
        return "Sub"
    def simplify(self):
       try:
        if equals(self.firstpart,self.secendpart):
            return Constant(0)
        if isinstance(self.firstpart,(Add,Sub)):
            fp=self.firstpart.firstpart
            sp=self.firstpart.secendpart
            if equals(fp,self.secendpart):
                return sp
            if equals(sp,self.secendpart):
                return fp
        if self.firstpart.simple == True and self.secendpart.simple == True or (self.getname()=="Ln" and self.simple==True):
            if (isinstance(self.firstpart, Mull) and isinstance(self.secendpart, Mull)):
                fp1 = self.firstpart.firstpart
                fp2 = self.firstpart.secendpart
                sp1 = self.secendpart.firstpart
                sp2 = self.secendpart.secendpart
                if equals(fp1, sp1) and isinstance(fp1, Var) and fp2.equaltype(sp2) and isinstance(fp2, Constant):
                    return Mull(Constant(fp2.getnum() - sp2.getnum()), Var)
                if equals(fp1, sp2) and isinstance(fp1, Var) and fp2.equaltype(sp1) and isinstance(fp2, Constant):
                    return Mull(Constant(fp2.getnum() - sp1.getnum()), Var())
                if fp1.equaltype(sp1) and isinstance(fp1, Constant) and fp2.equaltype(sp2) and isinstance(fp2, Var):
                    return Mull(Constant(fp1.getnum() - sp1.getnum()), Var())
                if fp1.equaltype(sp2) and isinstance(fp1, Constant) and fp2.equaltype(sp1) and isinstance(fp2, Var):
                    return Mull(Constant(fp1.getnum() - sp2.getnum()), Var())
            if isinstance(self.firstpart, Mull):
                if (isinstance(self.firstpart.firstpart, Constant) and isinstance(self.firstpart.secendpart,
                                                                                  Var)) and equals(self.secendpart,
                                                                                                   Var()):
                    return Mull(Constant(self.firstpart.firstpart.getnum() - 1), Var())
                if (isinstance(self.firstpart.secendpart, Constant) and isinstance(self.firstpart.firstpart,
                                                                                   Var)) and equals(self.secendpart,
                                                                                                    Var()):
                    return Mull(Constant(self.firstpart.secendpart.getnum() - 1), Var())
            if isinstance(self.secendpart, Mull):
                if (isinstance(self.secendpart.firstpart, Constant) and isinstance(self.secendpart.secendpart,
                                                                                   Var)) and equals(self.firstpart,
                                                                                                    Var()):
                    return Mull(Constant(self.secendpart.firstpart.getnum() - 1), Var())
                if (isinstance(self.secendpart.secendpart, Constant) and isinstance(self.secendpart.firstpart,
                                                                                    Var)) and equals(self.firstpart,
                                                                                                     Var()):
                    return Mull(Constant(self.secendpart.secendpart.getnum() - 1), Var())
            if not (isinstance(self.firstpart, (Var, Constant)) or isinstance(self.secendpart, (Var, Constant))):
                self.simple = True
            elif isinstance(self.firstpart, (Var, Constant)) and isinstance(self.secendpart, (Sub, Add)) and (
                    isinstance(self.secendpart.firstpart, (Var, Constant)) or isinstance(self.secendpart.secendpart,
                                                                                         (Var, Constant))
            ):
                fp = self.secendpart.firstpart
                sp = self.secendpart.secendpart
                if fp.equaltype(self.firstpart) and not isinstance(self.secendpart, (Expo, Mull)):
                    if not self.secendpart.equaltype(Sub(1, 1)):
                        return Add(Sub(fp, self.firstpart).simplify(), sp)
                    else:
                        return Add(Add(fp, self.firstpart).simplify(), sp)
                if sp.equaltype(self.firstpart):
                    if not self.secendpart.equaltype(Sub(1, 1)):
                        return Add(Sub(sp, self.firstpart).simplify(), fp)
                    else:
                        return Add(Add(sp, self.firstpart).simplify(), fp)
            elif not isinstance(self.firstpart, (Var, Constant,Expo)) :
                fp = self.firstpart.firstpart
                sp = self.firstpart.secendpart
                if fp.equaltype(self.secendpart) and not isinstance(self.secendpart, (Expo, Mull)):
                    if not self.firstpart.equaltype(Sub(-1, 1)):
                        return Sub(Sub(fp, self.secendpart).simplify(),Mull(-1,sp))
                    else:
                        return Sub(Add(fp, self.secendpart).simplify(),Mull(-1,sp))
                if sp.equaltype(self.secendpart) and not isinstance(self.firstpart, (Expo, Mull)):
                    if not self.firstpart.equaltype(Sub(-1, 1)):
                        return Sub(Sub(sp, self.secendpart).simplify(),Mull(-1,fp))
                    else:
                        return Sub(Add(sp, self.secendpart).simplify(), Mull(-1,fp))
            elif isinstance(self.firstpart,(Mull,Expo)) or isinstance(self.secendpart,(Mull,Expo)):
                self.simple=True
                return self
        if not (isinstance(self.firstpart, (Var, Constant)) and isinstance(self.secendpart, (Var, Constant))) and self.firstpart.simple==False:
            return Sub(self.firstpart.simplify(), self.secendpart.simplify()).simplify()
        if isinstance(self.firstpart, Constant) and isinstance(self.secendpart, Constant):
            return Constant(self.firstpart.getnum() - self.secendpart.getnum())
        if isinstance(self.firstpart, Var) and isinstance(self.secendpart, Var):
            return Constant(0)
        if equals(self.secendpart,Constant(0)):
            return self.firstpart
        if equals(self.firstpart,Constant(0)):
            return Mull(-1,self.secendpart)
        if isinstance(self.secendpart,Constant) and self.secendpart.getnum()<0:
            return Add(self.firstpart,-1*self.secendpart.getnum())
        if (isinstance(self.firstpart, (Expo,Mull,Add, Sub)) or isinstance(self.secendpart, (Expo,Mull,Add, Sub))) and self.simple == False:
            if isinstance(self.firstpart, (Var, Constant)):
                return Sub(self.firstpart, self.secendpart.simplify()).simplify()
            else:
                return Sub(self.firstpart.simplify(), self.secendpart).simplify()
        self.simple = True
        return self
       except RecursionError as e:
           return self
class Expo(Expression):
    def __init__(self,base,exponent,simple=None):
        self.base=base
        self.exponent=exponent
        self.simple=simple
        if isinstance(self.base,(int,float)):
            self.base=Constant(base)
        if isinstance(self.exponent,(int,float)):
            self.exponent=Constant(exponent)
        if self.simple is None:
            self.simple=False
    def evaluate(self,x_value):
        if (type(x_value) == int or type(x_value) == float):
            if not equals(self.exponent,Constant(-1)) or self.base.evaluate(x_value)!=0:
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
      if (isinstance(self.exponent,(Add,Sub,Mull,Expo))) and isinstance(self.base,Constant):
          return Mull(self,Mull(Constant(ln(self.base.getnum())),self.exponent.getderivative()))
      if isinstance(self.exponent,Constant):
          return Mull(self.base.getderivative(),Mull(self.exponent,Expo(self.base,self.exponent.getnum()-1)))
      raise NotSupportedException("we dont support x^x  integrals or derivatives|derivative error")
    def tostring(self):
     if self.exponent.equaltype(Constant(1)) and self.exponent.getnum()<0:
         temp=-1*self.exponent.getnum()
         temp=Constant(temp)
         return "(1/("+self.base.tostring()+")^{"+temp.tostring()+"})"
     return  f"{self.base.tostring()}^{{{self.exponent.tostring()}}}"
    def __str__(self):
        return self.tostring()
    def integral(self):
        if type(self.base)==Constant and (type(self.exponent) == Var or type(self.exponent) == Add or type(self.exponent) == Sub or type(self.exponent) == Expo
        or type(self.exponent) == Mull):
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
        if equals(self.exponent,Constant(-1)):
            return Ln(self.base)
        if self.exponent.tostring() != "x" and not isinstance(self.exponent,(Sub,Add,Expo,Mull)):
            return Mull(Constant(1/(self.exponent.getnum()+1)),Expo(Var(),Constant(self.exponent.getnum()+1)))
        if isinstance(self.base, Constant) and isinstance(self.exponent, Var):
            return Mull(Expo(self.base,Var()),Constant(1 / ln(self.base.getnum())))
        raise NotSupportedException("we dont support x^x integrals or derivatives|integral error")
    def equaltype(self,other):
        return isinstance(other,Expo)
    def getname(self):
        if equals(self.exponent,Constant(-1)):
         return "Div"
        return "Expo"
    def simplify(self):
       try:
        if equals(self.base,Constant(0)):
            return Constant(0)
        if equals(self.exponent,Constant(0)):
            return Constant(1)
        if equals(self.exponent,Constant(1)):
            return self.base
        if isinstance(self.base,Constant) and self.base.equaltype(self.exponent) :
            try:
             if self.exponent.getnum()<=1000:
              return Constant(round(self.base.getnum()**self.exponent.getnum(),4))
             else:
                 raise ELNException
            except ELNException as e:
                print("number far too large to fully simplify")
                self.simple=True
                pass
        if isinstance(self.base, Constant) and isinstance(self.exponent, (Mull, Sub, Expo, Add)) and isinstance(
                self.exponent.simplify(), Constant):
            if isinstance(self.exponent,Expo) and self.exponent.simplify().getnum() <= 1000:
                return Constant(self.base.getnum()**self.exponent.base.getnum()**self.exponent.exponent.getnum())
            elif self.exponent.simplify().getnum() <= 1000:
             return Constant(self.base.getnum()**self.exponent.simplify().getnum())
        if self.base.simple==True and self.exponent.simple==True:
            self.simple=True
        if isinstance(self.exponent,(Sub,Add,Mull,Expo)) and isinstance(self.base,(Constant,Var)) and self.simple==False:
            return Expo(self.base,self.exponent.simplify()).simplify()
        if isinstance(self.base,(Sub,Add,Mull,Expo)) and isinstance(self.exponent,(Constant,Var)) and self.simple==False:
            return Expo(self.base.simplify(),self.exponent).simplify()
        if isinstance(self.base,(Sub,Add,Mull,Expo)) and isinstance(self.exponent,(Sub,Add,Mull,Expo)) and self.simple==False:
            return  Expo(self.base.simplify(),self.exponent.simplify()).simplify()
        if not self.exponent.simple:
            return Expo(self.base,self.exponent.simplify())
        self.simple=True
        return self
       except RecursionError as e:
          return self
def random_expression(depth=None,Type=None):
    if depth==None:
        depth=random.randint(2,15)

    if depth<=0:
        coin=random.randint(0,1)
        if coin==0:
            return Var()
        else:
            return Constant(random.randint(1,30))
    else:
        type = random.choice(['Add', 'Sub', 'Mull', 'Expo','Div','Ln'])
        if Type in ['Add', 'Sub', 'Mull', 'Expo','Div','Ln']:
            type=Type
        leftdepth=random.randint(0,depth-1)
        rightdepth= depth -1 - leftdepth
        left = random_expression(leftdepth)
        right = random_expression(rightdepth)
        if type=='Add':
            return Add(left,right)
        if type=='Sub':
            return Sub(left,right)
        if type=='Mull':
            return Mull(left,right)
        if type=='Expo':
            if not equals(Expo(left,right),Expo(x,x)):
             return Expo(left,right)
            else:
                left = random_expression(leftdepth)
                right = random_expression(rightdepth)
                return Expo(left,right)
        if type=='Div':
            return Div(left,right)
        if type=='Ln':
            coin=random.randint(1,2)
            if coin==1:
             return Ln(left)
            if coin==2:
             return Ln(right)
class Div(Expression):
    def __new__(cls,firstpart,secendpart=None):
        if secendpart==None and firstpart==0:
             raise InvalidNumException("Division by zero not allowed")
        return super().__new__(cls)
    def __init__(self,firstpart,secendpart=None,simple=None): #firstpart=numerator , secendpart=denumarator.
        self.firstpart=firstpart
        self.secendpart=secendpart
        if isinstance(firstpart,(int,float)):
            self.firstpart=Constant(firstpart)
        if isinstance(secendpart,(int,float)):
            self.secendpart=Constant(secendpart)
        if equals(Constant(0),self.secendpart):
            raise ZeroDivisionError("Division by zero not allowed")
        if simple==None:
            self.simple=False
    def evaluate(self,x_value):
        if (type(x_value) == int or type(x_value) == float):
            if self.secendpart.evaluate(x_value) != 0:
             return self.firstpart.evaluate(x_value)/self.secendpart.evaluate(x_value)
        else:
            raise InvalidCombinationException("evaluate doesnt accept non number types or out of bounds")
    def tostring(self):
        return f"({self.firstpart.tostring()} / {self.secendpart.tostring()})"
    def __str__(self):
        return self.tostring()
    def getname(self):
        return "Div"
    def equaltype(self,obj):
        return isinstance(obj,Div)
    def getderivative(self):
        return Div(Sub(Mull(self.firstpart.getderivative(),self.secendpart),Mull(self.firstpart,self.secendpart.getderivative())),Expo(self.secendpart,2))
    def integral(self):
        if self.firstpart.equaltype(Constant(1)) and self.secendpart.equaltype(Constant(1)):
            return Mull(x,self.firstpart.getnum()/self.secendpart.getnum())
        if self.firstpart.equaltype(Constant(1)) and isinstance(self.secendpart, (Add, Sub, Var,Mull)):
            if self.secendpart.equaltype(Var()):
                return Mull(self.firstpart,Ln(self.secendpart))
            if self.secendpart.equaltype(Mull(1,1)):
                if  (isinstance(self.secendpart.firstpart,(Constant)) or isinstance(self.secendpart.secendpart,Constant))\
                        and (self.secendpart.firstpart.equaltype(x) or self.secendpart.secendpart.equaltype(x)):
                    if self.secendpart.firstpart.equaltype(Constant(1)):
                        return Mull(self.firstpart.getnum()/self.secendpart.firstpart.getnum(),Ln(x))
                    else:
                        return Mull(self.firstpart.getnum()/self.secendpart.secendpart.getnum(),Ln(x))
        if equals(self.firstpart.fully_simplify(), self.secendpart.getderivative().fully_simplify()):
            return Ln(self.secendpart)
        if equals(Constant(-1),self.secendpart.getderivative().fully_simplify()):
            return Mull(-1,Ln(self.secendpart))
        if self.secendpart.equaltype(Constant(1)):
            return Mull(Div(self.secendpart),self.firstpart.integral())
        if self.firstpart.equaltype(Constant(1)) and self.secendpart.simplify().equaltype(Expo(1,1)) and \
            self.secendpart.simplify().exponent.equaltype(Constant(1)):
            return Mull(self.firstpart,Expo(self.secendpart.simplify().base,-1*self.secendpart.simplify().exponent.getnum())).integral()
        raise NotSupportedException("integral not supported")
    def simplify(self):
       try:
        if equals(self.secendpart.simplify(),Constant(0)):
            raise ZeroDivisionError("Division by zero not allowed")
        if equals(self.firstpart,self.secendpart):
            return Constant(1)
        if self.firstpart.equaltype(Constant(1)) and self.secendpart.equaltype(Constant(1)):
            return Constant(self.firstpart.getnum()/self.secendpart.getnum())
        if equals(self.firstpart,Constant(0)):
            return Constant(0)
        if equals(self.secendpart,Constant(1)):
            return self.firstpart
        if equals(self.secendpart,Constant(-1)):
            return Mull(-1,self.firstpart)
        if equals(self.firstpart,Var()) and self.secendpart.equaltype(Expo(1,1)) and self.secendpart.base.equaltype(Var()) and \
            self.secendpart.exponent.equaltype(Constant(1)):
            return Div(1,Expo(self.secendpart.base,self.secendpart.exponent.getnum()-1))
        if equals(self.secendpart,Var()) and self.firstpart.equaltype(Expo(1,1)) and self.firstpart.base.equaltype(Var()) and \
            self.firstpart.exponent.equaltype(Constant(1)):
            return Expo(self.firstpart.base,self.firstpart.exponent.getnum()-1)
        if isinstance(self.firstpart,(Mull)) and isinstance(self.secendpart,(Mull)):
            fp1=self.firstpart.firstpart
            sp1=self.firstpart.secendpart
            fp2=self.secendpart.firstpart
            sp2=self.secendpart.secendpart
            if equals(fp1,fp2):
                return Div(sp1,sp2).simplify()
            if equals(fp1,sp2):
                return Div(sp1,fp2).simplify()
            if equals(sp1,fp2):
                return Div(fp1,sp2).simplify()
            if equals(sp1,sp2):
                return Div(fp1,fp2).simplify()
        if  isinstance(self.firstpart,(Mull)):
            fp=self.firstpart.firstpart
            sp=self.firstpart.secendpart
            if equals(fp,self.secendpart):
                return sp
            if equals(sp,self.secendpart):
                return fp
        if  isinstance(self.secendpart,(Mull)):
            fp=self.secendpart.firstpart
            sp=self.secendpart.secendpart
            if equals(fp,self.firstpart):
                return Div(1,sp)
            if equals(sp,self.firstpart):
                return Div(1,fp)
        if self.firstpart.equaltype(self.secendpart) and self.firstpart.equaltype(Expo(1,1)):
            if equals(self.firstpart.base,self.secendpart.base):
                return Expo(self.firstpart.base,Sub(self.firstpart.exponent,self.secendpart.exponent).simplify())
        if self.firstpart.simple==True and self.secendpart.simple==True:
            self.simple=True
        if (isinstance(self.firstpart, (Expo, Mull, Add, Sub, Div, Ln)) or isinstance(self.secendpart, (
        Expo, Mull, Add, Sub, Div, Ln))) and self.simple == False:
            if (isinstance(self.firstpart, (Expo, Mull, Add, Sub, Div, Ln))):
                self.firstpart = self.firstpart.simplify()
            if (isinstance(self.secendpart, (Expo, Mull, Add, Sub, Div, Ln))):
                self.secendpart = self.secendpart.simplify()
            return Div(self.firstpart, self.secendpart).simplify()
        self.simple=True
        return self
        # cant think of other ways to integrate Div
       except (RecursionError):
           return self
class Ln(Expression):
    def __new__(cls,expression):
        if isinstance(expression,(float,int)):
            expression=Constant(expression)
        if expression.equaltype(Expo(1,1)) and (expression.base.equaltype(Constant) or isinstance(expression.base,(int,float))):
            if expression.base.equaltype(Constant) and ln(expression.base.getnum()) == 1:
                return expression.exponent
            if isinstance(expression.base,(int,float)) and ln(expression.base) == 1:
                return expression.exponent
        return super().__new__(cls)
    def __init__(self,expression,simple=None):
        self.expression=expression
        if isinstance(expression,(float,int)):
            self.expression=Constant(expression)
        if self.expression.equaltype(Constant(1)) and self.expression.getnum() < 0:
            raise InvalidNumException("Ln cannot be less than zero")
        if simple==None:
             self.simple=False
    def getname(self):
        return "Ln"
    def evaluate(self,x_value):
        if (type(x_value) == int or type(x_value) == float):
            if self.expression.evaluate(x_value)>0:
             return ln(self.expression.evaluate(x_value))
        else:
            raise InvalidCombinationException("evaluate doesnt accept non number types or out of bounds")
    def equaltype(self,obj):
        return isinstance(obj,Ln)
    def getderivative(self):
        return Div(self.expression.getderivative(),self.expression)
    def tostring(self):
        return f"Ln({self.expression})"
    def __str__(self):
        return self.tostring()
    def integral(self):
        if isinstance(self.expression,Constant):
            return Mull(x,Ln(self.expression))
        if isinstance(self.expression,(Var)):
            return Sub(Mull(self.expression,Ln(self.expression)),self.expression)
        if isinstance(self.expression,(Add,Sub,Mull)) and isinstance(self.expression.firstpart,(Var,Constant)) and isinstance(self.expression.secendpart,(Var,Constant)):
            return Sub(Mull(x,Ln(self.expression)),Mull(x,self.getderivative()).integral())
        #only simple integrals for Ln(g(x))
    def simplify(self):
           try:
            if self.expression.equaltype(Constant(1)):
                return Constant(ln(self.expression.getnum()))
            if self.expression.equaltype(Expo(1, 1)) and self.expression.base.equaltype(Constant(1)) and ln(
                    self.expression.base.getnum()) == 1:
                return self.expression.exponent.simplify()
            if self.expression.equaltype(Expo(1, 1)):
                return Mull(self.expression.exponent, Ln(self.expression.base.simplify()))
            if self.expression.equaltype(Mull(1, 1)):
                return Add(Ln(self.expression.firstpart), Ln(self.expression.secendpart))
            if self.expression.equaltype(Div(1)):
                return Sub(Ln(self.expression.firstpart), Ln(self.expression.secendpart))
            if self.expression.simple == False:
                return Ln(self.expression.simplify())
            self.simple = True
            return self
           except RecursionError:
               return self
 # need to add div simplify for a**x / b**x = (a/b)**x
#shortcuts
x = Var()
e=ePower(1)
pie=3.1415926535
func =(x**2)-1
