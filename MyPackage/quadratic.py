# -*- coding: utf-8 -*-
"""
(Excuse language errors as english isn't my first language)
The Purpose of this libary is to give accsess to multiple operations on quadratics functions.
 These can be written in two ways in order to work in for them to work with these methods:
1) written in a tuple in the form (a,b,c) as to refrence ax^2 +bx + c and works for almost all methods until mentioned otherwise. for example Roots((a,b,c))
can be written in the first input of the method, the method needs  just the function itself, no need to write b,c aswell in the other inputs.
2) written Stright up inside the method as (a,b,c) as to refrence ax^2 +bx +c aswell.
 works for almost all methods until mentioned otherwise. for example Area(a,b,c) works the same as the last Area example.

(all parameters who can be represented as floats can be inputted as ints as well)
this is also my first library so try to excuse my methods names, the fact that it's a method only
libary aswell and my  somewhat unprofessional descriptions to the functions.(if anyone sees this constructive criticism is welcome).

"""
class quadraticExpection(Exception):
    pass


class IntegralException(quadraticExpection):
    def __init__(self):
        super().__init__("Cant integrate past x^3")
class InvalidNumException(quadraticExpection):
    def __init__(self):
        super().__init__("Function is invalid")
# i wrote these notes and code on my own incase you think i copied this from chatgpt
# heavly reccomend use of tuples for the functions.most of these operands you can just type in a,b,c but some require you to use them in tuple format(a,b,c) (like Interception)
def Roots(a:float,b:float=None,c:float=None):
    """
    The purpose of this method is to return the Roots of a function ax^2 +bx +c = 0 
    Parameters:
          a=x^2,function (float or tuple representing (a,b,c))
          b=x (float or None with tuple option)
          c=c (float or None with tuple option)
    Returns:
    -Returns none if there are no Roots
    -for a single root returns a tuple with the answer in float
    -for 2 roots returns a tuple with both of the answers in float.
    Examples:
        >>> Roots(1, -3, 2)
        (2.0, 1.0)
        >>> Roots((1, 2, 1))
        (-1.0,)
        >>> Roots(1, 0, 1)
        None

    """
    if isinstance(a,tuple):
       if len(a) == 3:
         temp=a
         a=temp[0]
         b=temp[1]
         c=temp[2]
    try:
        if _check(a, b, c) == False:
            raise InvalidNumException()
    except InvalidNumException as e:
        print(e)
        return
    #check if answers exist
    Discrim=(b**2)-4*a*c
    if Discrim<0:
        return None
    #skip if a==0 to save runtime and we cant divide by zero later on
    if a==0 and b != 0:
        return tuple([-(c/b)])
    # if c!=0 c==0 has no answers
    elif a==0 and b==0:
        return None
    #classic root equation
    a2=a*2
    answer1=(-b+(Discrim)**0.5)/a2
    answer2=(-b-(Discrim)**0.5)/a2
    if (answer2 != answer1):
     return (answer1,answer2)
    else:
        return tuple([answer1])


def max_min(a:float,b:float=None,c:float=None):
    """
    The purpose of this method is to return the Maximum/Minimum point in a function ax^2 +bx+c (if it exists)
    Parameters:
         a=x^2,function (float or tuple representing (a,b,c))
         b=x (float or None with tuple option)
         c=c (float or None with tuple option)
    Returns:
        -returns None if the function has no Maximum or Minimum point (typically when a==0)
        -returns a dic with the format {"x": x coordinate, "y": y coordinate, "type": type} where type is either a Maximum or Minimum
    Examples:
        >>> max_min(1, -4, 3)
       {'x': 2.0, 'y': -1.0, 'type': 'minimum'}
        >>> max_min(-2, 8, -3)
       {'x': 2.0, 'y': 5.0, 'type': 'maximum'}
       >>> max_min((0, 5, 2))
       None
    """
    if isinstance(a,tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            b = temp[1]
            c = temp[2]
    try:
        if _check(a, b, c) == False:
            raise InvalidNumException()
    except InvalidNumException as e:
        print(e)
        return
    if a==0:
        return None
    answerx=-(b/(2*a))
    if a<0:
        type="maximum"
    else:
        type="minimum"
    answery=a*(answerx)**2 + b*answerx + c
    return {"x": answerx, "y": answery, "type": type}


def Derivative(a:float,b:float=None,c:float=None):
    """
    The purpose of this method is to return the Derivative of the function ax^2 +bx +c /ax^3 +bx^2 +cx + constant_d (second option is usually a result of an AntiDerivative)
    Parameters:
         a=x^2,function (float or tuple representing (a,b,c) or tuple representing (a,b,c,constant_d))
         b=x (float or None with both tuple options)
         c=c (float or None with both tuple options)
         d=  (Typically String but can be all types for it doesnt effect the result)
    Returns:
         -returns tuple of (0,2a,b) representing 0*x^2 +2ax + b when receiving a function of second degree and lower.
         -returns a tuple of coefficients (a,b,c) in the format ax^2 +bx +c when receiving a function of third degree
    Examples:
         >>> Derivative((2, 4, -1))
         (0, 4.0, 4)  
         >>> Derivative((1, 2, 3, 4))
         (3, 4, 3)  
    """
    if isinstance(a,tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            b = temp[1]
            c = temp[2]
        elif len(a) == 4:
            temp=a
            a=temp[0] * 3
            b=temp[1] *2
            c=temp[2]
            return (a,b,c)
    try:
        if _check(a, b, c) == False:
            raise InvalidNumException
    except InvalidNumException as e:
        print(e)
        return
    return (0,2*a,b)


def Intersection(equation1,equation2):
    """
    The purpose of this method is to return all X's where two equations intersect at (max 2 with quadratic equations).
    Parameters:
          equation1=first part of the equation ( function tuple (a,b,c) where a,b,c are floats or ints)
          equation2=second part of the equation ( function tuple (a,b,c) where a,b,c are floats or ints)
    Returns:
           -False if the equations arent in valid format or dont equal in length.
           -Returns None if there are Intersection points or infinite points
           -for a single point returns a tuple with a single x as floats
           -for 2 points returns a tuple with both x^s as floats
    Examples:
          >>> Intersection((1, -3, 2), (0, 0, 0))
          (2.0, 1.0)
          >>> Intersection((2, 0, 0), (-2, 0, 0))
          (0.0,)
          >>> Intersection((1, 0, 1), (1, 0, -1))
          None
          >>> Intersection((1, 3, 1), (1, 3, 1))
          None
          >>>Intersection((1,2),(1,2,3))
          False
    """
    if (type(equation2) != tuple or type(equation1) != tuple):
        return False
    if len(equation1) != len(equation2):
        return False
    newa=equation1[0] - equation2[0]
    newb=equation1[1] - equation2[1]
    newc=equation1[2] - equation2[2]
    return Roots(newa,newb,newc)


def getFunc(a,b,c): #based on ax^2 + bx + c

    """
    The purpose of this method is to return a quadratic function as a tuple
     Parameters:
         a=x^2 (float)
         b=x (float)
         c=c (float)
     Returns:
         -a tuple of (a,b,c)  
     Examples:
         >>>getFunc(1,2,3)
         (1,2,3)
    """
    try:
     if _check(a,b,c) ==True:
      return (a,b,c)
     else:
         raise InvalidNumException()
    except InvalidNumException as e:
        print(e)
        return




def _check(a,b,c):
    """
    The purpose of this method is to check if all parts of the function a,b,c are floats or ints. this method isn't public.
    Parameters:
         a=x^2 (float)
         b=x (float)
         c=c (float)
    Returns:
         -returns True if a,b,c are all float or int (can be mixed)
         -returns False if at least one of the Parameters isn't an int or float
    Examples:
          >>>_check(1,1.5,3)
          True
          >>>_check(1,"string",1.5)
          False      
    """
    if (type(a) != float and type(a) != int) or (type(b) != float and type(b) != int) or (type(c) != float and type(c) != int):
        return False
    return True


def Integral(a:float,b:float=None,c:float=None): #based on ax^3 + bx^2 +cx +d. #added a defenite integral option between two points and replaces b,c with d,e.
    """
    This method has 2 purposes:
    1.To compute and return the anti derivative of a function ax^2 +bx +c
    2.To compute and return the Definite integral of a function between 2 x values : from x b to x c
    we will go over each one.
    1.Anti derivative)
    Parameters:
        a=x^2,function (float or tuple represting (a,b,c)
        b=x (float or None with tuple option)
        c=c (float or None with  tuple option)
    Returns:
        -a new tuple with length 4 (a,b,c,"d") represnting the AntiDerivative ax^3 +bx^2 +cx + constant_d (these a,b,c are different floats to the ones inputted in the method
        while d is returned as a string "d")
    !Warning- cannot integrate past x^3 onward
    Examples:
         >>> Integral(3, 6, 9)
        (1.0, 3.0, 9, 'd')
        >>> Integral((3, 6, 9))
        (1.0, 3.0, 9, 'd')
    2.Definite integral)
    Parameters:
        a=function (tuple (a,b,c) with a,b,c being floats)
        b=x b (float)
        c=x c (float
    Returns:
          -the worth of the definite integral between 2 points as float
    Examples:
        >>> Integral((3, 6, 9), 0, 1)
        13.0  # The definite integral from 0 to 1              
    """
    d=b
    e=c
    if isinstance(a,tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            d = temp[1]
            e = temp[2]
            if ((type(b) == float or type(b) == int) and ((type(c) == float) or type(c) == int)):
             val=Integral(a,d,e)
             a = val[0]
             d=val[1]
             e=val[2]
             answer=(a*c**3)+(d*c**2)+(e*c)-((a*b**3)+(d*b**2)+(e*b))
             return answer
        else:
            try:
                if len(a) >3:
                    raise IntegralException()
            except IntegralException as e:
                print(e)
                return
    try:
     if _check(a,d,e) == False  :
        raise InvalidNumException
    except InvalidNumException as e:
        print(e)
        return
    if (d==None) :
     newa=a/3
     newb=b/2
     newc=c
    else:
     newa = a / 3
     newb = d / 2
     newc = e

   # print(f"tuple changes from (x^2,x,c) = ({a},{d},{e}) to (x^3,x^2,x,float d)=({newa},{newb},{newc},d)") #i thought it was Unssecery but maybe il add later
    return (newa,newb,newc,"d")
def Area(function:tuple,lowend:float,highend:float): #this is the defenite integral but with absolute value.
    """
    The purpose of this method is to Calculate the definite area under a quadratic curve between two x-values. from lowend to highend.
    Parameters:
        function=function (tuple (a,b,c) of floats)
        lowend= first x (float)
        highend= secend x (float)
    Returns:
        - the positive area under the curve
        - 0 if highend== lowend
    Examples:
        >>> Area((1, 0, 0), 1, 2)
        2.333333333333333
        >>> Area((1, 0, 0), 1, 1)
        0    
    """
    try:
        if type(function) != tuple:
            raise InvalidNumException
    except InvalidNumException as e:
        print(e)
    if highend==lowend:
        return 0
    integral=Integral(function)
    a=integral[0]
    b=integral[1]
    c=integral[2]
    calcs=abs((a*highend**3)+(b*highend**2)+(c*highend)-((a*lowend**3)+(b*lowend**2)+(c*lowend)))
    return calcs
def findY(a:float,b:float=None,c:float=None,x:float=None):
    """
    The purpose of this method is to calculate and return the y value of a function (a,b,c) at a given x.
    Parameters:
          a=x^2,function (float or tuple representing (a,b,c))
          b=x (float or None with tuple option)
          c=c (float or None with tuple option)
          x=point x on the function we want to calc the y value of (float)
    Returns:
          -the y value in float
    Examples:
          >>> findY(1, -3, 2, 4)
          6
          >>> findY((1,0,-4),0)
          -4
    """
    backup=b
    if isinstance(a, tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            x=backup
            b = temp[1]
            c = temp[2]
    try:
        if _check(a, b, c) == False or ((type(x) != int) and (type(x) != float)):
            raise InvalidNumException()
    except InvalidNumException as e:
        print(e)
        return
    return ((a*x**2)+(b*x)+c)
def tangentLine(a:float,b:float=None,c:float=None,x:float=None):
    """
    The purpose of this method is to return the function of a tangent line in a given function of the given x
    Parameters:
          a=x^2,function (float or tuple representing (a,b,c))
          b=x (float or None with tuple option)
          c=c (float or None with tuple option)
          x=point x on the function we want to calculate the tangent line (float)
    Returns:
          -the function of the tangent line in the (a,b,c) format.
    Examples:
           >>> tangentLine(1, -3, 2, 1)
           (0, -1.0, 2.0)
           >>> tangentLine((1, -3, 2), 1)
           (0, -1.0, 2.0)
    """
    backup=b
    if isinstance(a, tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            x=backup
            b = temp[1]
            c = temp[2]
    try:
        if _check(a, b, c) == False or ((type(x) != int) and (type(x) != float)):
            raise InvalidNumException()
    except InvalidNumException as e:
        print(e)
        return
    der=Derivative(a,b,c)
    slope=der[1]*x + der[2]
    return (0,slope,(-slope*x)+findY(a,b,c,x))
def funcInfo(a:float,b:float=None,c:float=None):
    """
    The purpose of this method is to return information about a given function regarding its roots,y axis interception value,its derivative and its maximum/minimum point.
    Parameters:
          a=x^2,function (float or tuple representing (a,b,c))
          b=x (float or None with tuple option)
          c=c (float or None with tuple option)
    Returns:
          -the info mentioned in the description of the function in the form of a string and takes 5 lines.
    Examples:
        >>> print(funcInfo(1, -3, 2))
        The function: (1, -3, 2) == 1x^2 +-3x +2
        Roots:(2.0, 1.0)
        y_intercept:2
        function_derivative:(0, 2.0, -3) == 2.0x + -3
        max/min point:{'x': 1.5, 'y': -0.25, 'type': 'minimum'}

        >>> print(funcInfo((1, 2, 1)))
        The function: (1, 2, 1) == 1x^2 +2x +1
        Roots:(-1.0,)
        y_intercept:1
        function_derivative:(0, 2.0, 2) == 2.0x + 2
        max/min point:{'x': -1.0, 'y': 0.0, 'type': 'minimum'}
    """
    if isinstance(a, tuple):
        if len(a) == 3:
            temp = a
            a = temp[0]
            b = temp[1]
            c = temp[2]
    try:
        if _check(a, b, c) == False:
            raise InvalidNumException()
    except InvalidNumException as e:
        print(e)
        return
    Root=Roots(a,b,c)
    ypoint=findY(a,b,c,0)
    externum=max_min(a,b,c)
    deri=Derivative(a,b,c)
    tostring=(f"The function: {(a,b,c)} == {a}x^2 +{b}x +{c}\n"
          f"Roots:{Root} \n"
          f"y_intercept:{ypoint}\n"
          f"function_derivative:{deri} == {deri[1]}x + {deri[2]}\n"
          f"max/min point:{externum}")
    return tostring
def Factors(a:float,b:float=None,c:float=None):
    """
    The purpose of this method is to return the factors of a given function (a,b,c) if they exist in this format:
    ((a,b,c),(d,e,f)) which represents (ax^2 +bx+c)(dx^2+ex+f) so essentially the two functions inside a tuple beside each-other.
    #warning! this can return the roots in a very non elegent way as my (a,b,c) format lacks the ability to represent functions with outside multiplications
    #such as constant*(a,b,c) see examples of this in examples
    Parameters:
          a=x^2,function (float or tuple representing (a,b,c))
          b=x (float or None with tuple option)
          c=c (float or None with tuple option)
    Returns:
          -if no real Factors exist returns None
          -if a=0 returns the function itself as its the factor of itself (technically)
          -if the factors are the same returns ((f(X),f(X))
          -if the factors are different returns ((f(x),g(x))
    Examples:
          >>> Factors(1, -3, 2)
          ((0, 1.0, -2.0), (0, 1.0, -1.0))

          >>> Factors((1, 2, 1))
          ((0, 1.0, -1.0), (0, 1.0, -1.0))

          >>> Factors(1, 1, 1)
          None
          #non elgent example
          >>>Factors(6,30,6.25)
          ((0, 2.449489742783178, 4.7821773229381925), (0, 2.449489742783178, 0.21782267706180777))
    """
    if isinstance(a,tuple):
       if len(a) == 3:
         temp=a
         a=temp[0]
         b=temp[1]
         c=temp[2]
    try:
        if _check(a, b, c) == False:
            raise InvalidNumException()
    except InvalidNumException as e:
        print(e)
        return
    rootcheck=Roots(a,b,c)
    if a==0:
        return (a,b,c)
    if rootcheck==None:
        return None
    if len(rootcheck) == 1:
        if a>0:
         return ((0,a**(0.5),-rootcheck[-1]),(0,a**(0.5),-rootcheck[-1]))
        if a<0:
         return ((0,-1*abs(a**(0.5)),rootcheck[-1]),(0,abs(a**(0.5)),-1*rootcheck[-1]))
    if len(rootcheck) == 2:
        if a > 0:
            return ((0, a ** (0.5), -rootcheck[-1]), (0, a ** 0.5, -rootcheck[-2]))
        if a < 0:
            return ((0, -1*abs(a ** (0.5)), rootcheck[-1]), (0, abs(a ** (0.5)), -1*rootcheck[-2]))

"""
Thank you for reading and potentially using my library in the future!!
"""