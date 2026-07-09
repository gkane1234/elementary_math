#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Created on Wed Feb 15 15:38:42 2023

@author: gkane
"""
from ast import Constant
import math
import random
import io
#from sympy import Matrix 
import re
from inspect import signature


class Polynomial:

    def __init__(self, terms=((0,0),),sort=True,simplify=True,latex=False,variable='x'):

        self.latex=latex
        superscript_map={"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶","7": "⁷", "8": "⁸", "9": "⁹"}
        
        self.trans = str.maketrans(''.join(superscript_map.keys()),''.join(superscript_map.values()))
            
        self.ROUNDING=10
        
        self.variable=variable
        
        #Terms is a tuple of tuples each interior tuple is (coeficient,exponent)
        
        if type(terms)==tuple and type(terms[0]==tuple):
            self.terms=terms
            
        if type(terms) in(list,tuple) and type(terms[0]) in (float, int, complex):
            terms=tuple([(j,i) for (i,j) in enumerate(reversed(terms))])
            a=Polynomial(terms,sort=sort)
            self.terms=a.terms

        if type(terms) in (float, int, complex):
            self.terms = ((terms,0),)
            
        if sort:
            self.sortTerms()
            
        if simplify:
            self.combineLikeTerms(constructor=True)

        self.degree=self.deg()
        
    def __round__(self,ndigits=None):
        if ndigits==None:
            ndigits=self.ROUNDING
        re=((0,0),)
        for (c,e) in self.terms:
            if type(c)==complex:
                cR=round(c.real,ndigits)
                cI=round(c.imag,ndigits)
                c=complex(cR,cI)
            else:
                c=round(c,ndigits)
            re+=((c,e),)
        return Polynomial(re,self).combineLikeTerms()
    def __repr__(self,latex=False,variable='x') :
        strin=''
        
        a=round(self)
        cC=0
        for (c,e) in a.terms:
            if type(c)==complex:
                cC=c.imag
                c=c.real
                
            if (c>=0):
                sign='+'
            else:
                sign=''
            if c==1:
                coef=''
            elif c==-1 and e>0:
                coef='-'
            else:
                coef=str(c)
            if e==0:
                x=''
                if c==1:
                    coef='1'
            elif e==1:
                x=variable
            else:
                if latex or self.latex:
                    x=variable+'^{'+str(e)+'}'
                else:
                    x=variable+self.sup(e)
            if cC:
                coef+=str(cC)+'j'
            strin+=sign+coef+x          
        return strin.lstrip('+')
    def __str__(self,rounding=5):
        a=round(self,rounding)
        return a.__repr__()
    def to_latex(self, rounding: int = 5) -> str:
        a = round(self, rounding)
        return a.__repr__(latex=True)

    def to_text(self, rounding: int = 5) -> str:
        """Plain-text representation (same as ``str``)."""
        return str(round(self, rounding))

    def outputWithNewVariable(self,rounding=5,var='x'):
        a=round(self,rounding)
        return a.__repr__(variable=var)
        return 
    def __mul__(self,other):
        if type(other)==Polynomial:
            retTerms=((0,0),)
            for (c1,e1) in self.terms:
                for (c2,e2) in other.terms:
                    retTerms+=((c1*c2,e1+e2),)
            return Polynomial(retTerms[1::]).combineLikeTerms()
        if type(other) in (int,float):
            retTerms=((0,0),)
            for (c1,e1) in self.terms:
                retTerms+=((c1*other,e1),)
            return Polynomial(retTerms[1::]).combineLikeTerms()
    def __rmul__(self,other):
        if type(other) in (int,float):
            return self.__mul__(other)
    def __add__(self,other):
        if type(other)==Polynomial:
            return Polynomial(self.terms+other.terms).combineLikeTerms()
        if type(other) in (int,float):
            n=(other,0)
            terms=self.terms
            terms+=(n,)
            return Polynomial(terms).combineLikeTerms()  
    def __radd__(self,other):
        if type(other) in (int,float):
            return self.__add__(other) 
    def __sub__(self,other):
        if type(other)==Polynomial:
            return self.__add__(other.__mul__(-1))
        if type(other) in (int,float):
            return self.__add__(-other)
    def __rsub__(self,other):
        if type(other) in (int,float):
            return self.__mul__(-1).__add__(other)
    def __pow__(self,other):
        if type(other) == (int):
            if other<0:
                print ("no")
            if other==1:
                return self
            if other==0:
                return Polynomial(((1,0),),variable=self.variable)
            
            return self.__mul__(self.__pow__(other-1))
    def __floordiv__(self,other):
        if type(other)==int:
            if other>0:
                if other==1:
                    newTerms=((),)
                    for (c,e) in self.terms:
                        if not e==0:
                            new=(c*e,e-1)
                            newTerms+=(new,)
                    return Polynomial(newTerms[1::])
                return (self//1)//(other-1)
            else:   
                if other==-1:
                        newTerms=((1,0),)
                        for (c,e) in self.terms:
                            new=(c/(e+1),e+1)
                            newTerms+=(new,)
                        return Polynomial(newTerms)
                return (self//-1)//(other+1)
    def __matmul__(self,other):
        if type(other) in (int,float,complex):
            return self.synthDiv(other)[1]

    def evaluate(self, x: float | int | complex) -> float | int | complex:
        """Evaluate the polynomial at *x* (remainder of synthetic division)."""
        return self @ x

    def synthDiv(self,k):
        
        a=self.coef_list()
        quo=[a[0]]
        for i in range(1,len(a)):
            quo.append(k*quo[i-1]+a[i])
        return (Polynomial(quo[:-1]),quo[-1])

    def poly_div(self, divisor):
        """Polynomial long division. Returns (quotient, remainder)."""
        if type(divisor) != Polynomial:
            raise TypeError("divisor must be a Polynomial")

        rem = [float(c) for c in self.coef_list()]
        div = [float(c) for c in divisor.coef_list()]

        while len(rem) > 1 and abs(rem[0]) < 1e-10:
            rem = rem[1:]
        while len(div) > 1 and abs(div[0]) < 1e-10:
            div = div[1:]

        if not div or all(abs(c) < 1e-10 for c in div):
            raise ValueError("Division by zero polynomial")

        if len(rem) < len(div):
            return Polynomial(((0, 0),)), self

        quotient_terms: dict[int, float] = {}

        while len(rem) >= len(div):
            if abs(rem[0]) < 1e-10:
                rem = rem[1:]
                if len(rem) < len(div):
                    break
                continue

            degree_diff = len(rem) - len(div)
            lead_coef = rem[0] / div[0]
            quotient_terms[degree_diff] = quotient_terms.get(degree_diff, 0.0) + lead_coef

            for index in range(len(div)):
                rem[index] -= lead_coef * div[index]

            while len(rem) > 1 and abs(rem[0]) < 1e-10:
                rem = rem[1:]

        if not rem or all(abs(c) < 1e-10 for c in rem):
            remainder = Polynomial(((0, 0),))
        else:
            remainder = Polynomial([round(c) if abs(c - round(c)) < 1e-8 else c for c in rem])
        quotient = Polynomial(
            tuple(
                (round(coef) if abs(coef - round(coef)) < 1e-8 else coef, degree)
                for degree, coef in sorted(quotient_terms.items(), reverse=True)
                if abs(coef) >= 1e-10
            )
            or ((0, 0),)
        )
        return quotient, remainder

    def divide(self, divisor):
        """Alias for polynomial long division."""
        return self.poly_div(divisor)

    def is_zero(self) -> bool:
        return all(abs(c) < 1e-10 for c in self.coef_list(reverse=True))
    def __eq__(self, o):
        if type(o)==Polynomial:
            return o.coef_list(reverse=True)==self.coef_list(reverse=True)
        return False
    def __len__(self):
        return len(self.terms)
    def sortTerms(self):
        self.terms=sorted(self.terms,reverse=True,key = lambda x: x[1])
    def combineLikeTerms(self,constructor=False):
        self.sortTerms()
        last=self.terms[0][1]
        newTerms=((),)
        new=self.terms[0]
        for (c,e) in self.terms[1::]:
            if e==last:
                new=(c+new[0],new[1])
            else:
                if new[0]!=0:
                    newTerms+=(new,)
                new=(c,e)
                last=e
        
        if new[0]!=0:
            newTerms+=(new,)    

        if len(newTerms)==1:
            if constructor==True: #allows to combine like terms in the constructor without causing depth error
                self.terms=((0,0),)
                return None
            return Polynomial(((0,0),))
        
        if constructor==True:
                self.terms=newTerms[1::]
                return None
        return Polynomial(newTerms[1::])
    def sup(self,toSup):
        return str(toSup).translate(self.trans)
    def deg(self): #Gives degree
        
        m=0
        for (c,e) in self.terms:
            if e>m:
                m=e;
        return m

    @property
    def degree_property(self) -> int:
        """Degree as a property (see also :attr:`degree` set at construction)."""
        return self.deg()

    def leading_coefficient(self) -> float | int | complex:
        """Coefficient of the highest-degree term."""
        if self.is_zero():
            return 0
        return self.coef_list()[0]

    @property
    def leading_coeff(self) -> float | int | complex:
        """Alias for :meth:`leading_coefficient`."""
        return self.leading_coefficient()
   
    def exists(self,deg,start=0): #Gives first instance of a term with that degree
        l=len(self.terms)
        for i in range(start,l):

            if self.terms[i][1]==deg:
                return i
        return -1
    
    def coef(self,deg,start=0): #Gives coefficient of the first instance of a term with that degree
        l=self.exists(deg)
        if l==-1:
            return 0
        return self.terms[self.exists(deg,start)]
    
    def coef_list(self, reverse: bool = False) -> list:
        coeffs = [0] * (self.degree + 1)
        for (c, e) in self.terms:
            coeffs[e] += c
        if reverse:
            return coeffs
        return list(reversed(coeffs))

    def gcd(self, other: Polynomial) -> Polynomial:
        """Greatest common divisor with another polynomial."""
        from .operations import polynomial_gcd
        return polynomial_gcd(self, other)

    def gcf(self, other: Polynomial) -> Polynomial:
        """Alias for :meth:`gcd`."""
        return self.gcd(other)

    def lcm(self, other: Polynomial) -> Polynomial:
        """Least common multiple with another polynomial."""
        from .operations import polynomial_lcm
        return polynomial_lcm(self, other)

    def content_gcd(self) -> int:
        """GCD of all integer coefficients."""
        from .operations import content_gcd
        return content_gcd(self)
    def PFD(self,others) : 
        
        prods=[]
        if type(others)==Polynomial:#Self is numerator, others is polynomial to factor
            others=others.factor()
        #Self is numerator, others are factorization of denominator
        l=len(others)
        for i in range(l):
           prods.append(Polynomial(((1,0),)))
           for j in range(l):
               if not i==j:
                  prods[i]*=others[j] 
        
            
        degree=(prods[0]*others[0]).deg()
        
        coefs=[]
        diffs=[]
        for i in prods:
            termCoef=i.coef_list(reverse=True)
            diff=degree-len(termCoef)
            diffs.append(diff)
            for j in range(diff+1):
                coefs.append(
                    ([0]*(j))+termCoef+([0]*(diff-j)))
                
        thisCoefs=self.coef_list(reverse=True)+([0]*(degree-len(self.coef_list(reverse=True))))
        coefs.append(thisCoefs)
        
        from sympy import Matrix
        m=Matrix(coefs)
        
        m=m.transpose()
        
        values=m.rref()
        p=0
        
        polies=[]
        for i in diffs:
            poly=((0,0),)
            
            for j in range(i+1):
                poly+=((values[0][p+j,-1],j),)
            polies.append(Polynomial(poly[1::]))
            p+=i+1
        
        ret=''
        l=len(polies)
        
        for i in range(l):
            ret+=("("+str(polies[i])+")/("+str(others[i])+")+")
        return "("+self.__str__()+")/("+str(prods[0]*others[0])+")="+ret.rstrip('+')
    def solve(self) :
        
        if self.degree>4:
            raise NotImplementedError()
        x=self.coef_list()
        if self.degree==1:
            return (-x[1]/x[0],)
        elif self.degree==2:
            
            root=((x[1]**2-4*x[0]*x[2])**(1/2))/(2*x[0])
            vert=-x[1]/(2*x[0])
            
            return (vert+root,vert-root)
        elif self.degree==3:
            a=x[0]
            b=x[1]
            c=x[2]
            d=x[3]
            del0=(b**2)-3*a*c
            del1=2*(b**3)-9*a*b*c+27*(a**2)*d
            C=((del1+((del1**2-4*(del0**3)**(1/2))))/2)**(1/3)
            
            ep=(-1+((-3)**(1/2)))/2
            
            root=[]
            for k in range(3):
                root.append(-1/(3*a)*(b+(ep**k)*C+del0/((ep**k)*C)))
            
            return tuple(root)
        elif self.degree==4:
            a=x[0]
            b=x[1]
            c=x[2]
            d=x[3]
            e=x[4]
            
            p=(8*a*c-3*b**2)/(8*(a**2))
            q=(b**3-4*a*b*c+8*(a**2)*d)/(8*(a**3))
            
            del0=c**2-3*b*d+12*a*e
            del1=2*c**3-9*b*c*d+27*b**2*e+27*a*d**2-72*a*c*e
            
            Q=((del1+((del1**2-4*del0**3)**(1/2)))/2)**(1/3)
            
            S=1/2*((-2/3*p+1/(3*a)*(Q+del0/Q))**(1/2))
            
            t=-b/(4*a)
            v1=1/2*((-4*(S**2)-2*p+q/S)**(1/2))
            v2=1/2*((-4*(S**2)-2*p-q/S)**(1/2))
            
            return (t-S+v1,t-S-v1,t+S+v2,t+S-v2)
        return "Why did you try to solve a constant function?"    
    def deComplexify(self,others,rounding=None): #Takes complex numbers with no complex part and makes them real
        others=list(others)
        if rounding==None:
            rounding=self.ROUNDING
        l=len(others)    
        for i in range(l):
            o=others[i]
            if type(o)==complex:
                if round(o.imag,rounding)==0:
                    others[i]=o.real
        return tuple(others)
    def deComplexifyCoefficients(self,rounding=None,real=True) :
        a=self.coef_list()
        if real:
            return Polynomial([coef.real for coef in a])
        
        return Polynomial(self.deComplexify(a,rounding))
       
    def factor(self,real=True):

        if self.degree>1:
            (p,q)=self.findOneRootPair(real)
            
            #print(q,q.factor(real))
            #print(p)
            return (p,)+q.factor(real)
        if self.degree==4:
            b=self.solve()
            b=self.deComplexify(b)
            factors=(Polynomial([1,-b[0]]),Polynomial([1,-b[1]]),Polynomial([1,-b[2]]),Polynomial([1,-b[3]]))
            if real:
            
                if type(b[0])==complex:
                    factors1=(factors[0]*factors[1],)
                else:
                    factors1=(factors[0],factors[1])
                if type(b[2])==complex:
                    factors2=(factors[2]*factors[3],)
                else:
                    factors2=(factors[2],factors[3])
                return (factors1+factors2)
            
            return factors
        if self.degree==3:
           # self.deComplexifyCoefficients()
            b=self.solve()
            b=self.deComplexify(b)
            
            factors=Polynomial([1,-b[0]]),Polynomial([1,-b[1]]),Polynomial([1,-b[2]])
            if real:
                if type(b[1])==complex:
                    factors1=(factors[1]*factors[2],)
                else:
                    factors1=(factors[1],factors[2])
                return ((factors[0],)+factors1)
            return factors
        
        if self.degree==2:
            a=self.coef_list()[0]
            b=self.solve()
            b=self.deComplexify(b)
            if real and type(b[0])==complex:
                return (Polynomial([a]),(Polynomial([1,-b[0]])*Polynomial([1,-b[1]])).deComplexifyCoefficients(real=True),)

            return (Polynomial([a]),Polynomial([1,-b[0]]),Polynomial([1,-b[1]]))
        if self.degree<=1:
            return (self,)
    def findOneRootPair(self,real=True): #When degree is greater than 4
        
        deriv=self//1 #first derivative
        
        
        #first try to find a real root
        
        guess=random.random()
        candidate= self.newton(guess,deriv)
        #print("we found real:"+str(candidate))
        #then try to find a complex one
        
        while candidate==None:
            guess=complex(random.random(),random.random())
            candidate=self.newton(guess,deriv)
            
            
        root=self.deComplexify(((candidate),))[0]
                            
        if type(root)==complex:
            factors=(Polynomial([1,-root]),Polynomial([1,-(root.conjugate())]))
            rem=((self.synthDiv(root)[0]).synthDiv(root.conjugate()))[0]

            rem=rem.deComplexifyCoefficients(real=real)

            if real:
                return (factors[0]*factors[1],rem)
            return (factors,rem)
        fact=Polynomial([1,-root])
        rem=(self.synthDiv(root)[0])
        return (fact,rem)
    
    def newton(self,g,deriv,TOLERANCE=1e-10,maxV=1e8,max_attempts=200):
        attempts=0
        n=self@g
        while not ((type(n)==complex and (abs(n.real)<TOLERANCE and abs(n.imag)<TOLERANCE)) \
            or (not type(n)==complex and abs(n)< TOLERANCE)): #checks to see if it is a real root
            attempts+=1
            s=(deriv@g)
            
            if type(s)==float and math.isnan(s):
                return None
            
            try:
                if (attempts<max_attempts) \
                    and not (type(s)==complex and (s.real==0 or s.imag==0)) \
                    and not ((type(s) in (float,int)) and s==0)\
                    and not abs(s)>maxV:
                    
                    g-=(self @ g)/(s) #Newton's method
                    print(str(attempts)+":\t"+str(g))
                else:
                    return None
            except:
                print('(#@^$@(*#&%^(*@#&$^)!(@*#&)(#*@$&@(*#%&@#(*$&)!#(*&@)(#*&)@#(*%&@)(*#$&!)(*@#&whoops')
                return None
            n=self@g
        return g

    @staticmethod
    def displayFactors(others):
        print(others)
        if hasattr(others, '__iter__'):
            
            return '('+print_to_string(*others,sep=')(',end='')+')'
        
        return '('+str(others)+')'
    @staticmethod
    def createPolynomialWithIntegerFactorsRanges(leadingCoefficientRange,coefficientRange,factors,returnFactors=False,positiveLeadingCoefficient=True):
        #Creates a polynomial by multiplying together a bunch of factors 
        #Both ranges should be non-negative
        
        p=Polynomial([1])
        
        minLead,maxLead=leadingCoefficientRange
        minCoef,maxCoef=coefficientRange
        
        factorList=[]
        
        for i in range(1,factors+1):
            leadingCoefficient=random.randint(minLead, maxLead) if positiveLeadingCoefficient else 2*random.randint(0, 1)-1*random.randint(minLead, maxLead)
            constant = 2*random.randint(0, 1)-1*random.randint(minCoef, maxCoef)
            g=Polynomial([leadingCoefficient,constant])
            
            if returnFactors:
                factorList.append(g)
            p*=g
        if returnFactors:
            return (p,factorList)
        return (p)
    @staticmethod
    def maximumCoeficient(p) :
        m=0
        for i in p.terms:
            if abs(i[0])>m:
                m=abs(i[0])
                
        return m;
    
    @staticmethod
    def quadraticFactoringQuestions(num=1,cCoefficients=(-10,10),aCoefficients=(1,1)):
        quadratics = []
        
        for i in range(num):
            a=Polynomial.createPolynomialWithIntegerFactorsRanges(aCoefficients,cCoefficients,1)    
            b=Polynomial.createPolynomialWithIntegerFactorsRanges(aCoefficients,cCoefficients,1)
            quadratics.append(a*b)
        return quadratics
    
    @staticmethod 
    def cosineDoubleAnglePolynomial(powerOfTwo,p:None) :
        
        if p==None:
            p=Polynomial([1,0],variable="cos(x/2)")
        if powerOfTwo==0:
            return p
        return Polynomial.cosineDoubleAnglePolynomial(powerOfTwo-1,2*(p**2)-1)
    @staticmethod
    def productOfCosineDoubleAngles(maxPowerOfTwo) :
        p=Polynomial([1],variable='cos(x/2)')
        for i in range(maxPowerOfTwo):
            p*=Polynomial.cosineDoubleAnglePolynomial(i)
        print(p.outputWithNewVariable(var='cos(x/2)'))
        return p
    @staticmethod 
    def rrt(minV,maxV,terms=4, nonOneTerms = 0, maximumCoefficient = 20,irreducibleQuadratics = 0) :
        a= Polynomial(1)
        for j in range(terms)  :
            if j<nonOneTerms :
                a*=Polynomial((Polynomial.randomCoefficient(minV, maxV),Polynomial.randomCoefficient(minV, maxV)))
            else:
                a*=Polynomial((1,Polynomial.randomCoefficient(minV, maxV)))
                
        for j in range(irreducibleQuadratics) :
            b= Polynomial.randomCoefficient(minV, maxV)
            c= Polynomial.randomCoefficient(minV, maxV)
            if c>0:
                e=math.floor(b*b/(4*c))+2
            else:
                e= math.floor(b*b/(4*c))-2
                
                
            a*=Polynomial((c,b,e))
            

        if Polynomial.maximumCoeficient(a)>maximumCoefficient:
            return Polynomial.rrt(minV,maxV,terms,nonOneTerms,maximumCoefficient,irreducibleQuadratics)
        return a

    @staticmethod
    def differences(degree, values,step=1,start=1):
        
        a = Polynomial((Polynomial.randomCoefficient(-3,3,degree)))
        
        string = "\\begin{table}[]\n\\begin{tabular}{|l|l|}\n\cline{1-2}"


        for i in range(start,values+start*step,step) :
            #print(str(i)+"    "+str(a@i))
            string+=str(i)+"&"+str(a@i)+"\\\\\cline{1-2}"
        
        string+="\n\end{tabular}\n\end{table}"
        
    @staticmethod
    def randomCoefficient(minV,maxV,values=1,nonZero=True) :
        ret= ()
        for i in range(values):
            
            
            a=random.randint(minV,maxV)
            if a==0 and nonZero:
                a=Polynomial.randomCoefficient(minV,maxV)
            ret+=(a,)
        if values==1:
            return ret[0]
        return ret

    @staticmethod
    def randomPolynomial(degree, coef_min, coef_max, positive_leading=True):
        if degree < 0:
            return Polynomial(((0, 0),))

        coeffs = [
            Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)
            for _ in range(degree + 1)
        ]
        if positive_leading and coeffs[0] < 0:
            coeffs[0] *= -1
        return Polynomial(coeffs)

    @staticmethod
    def random_polynomial(degree, coef_min, coef_max, positive_leading=True):
        """Snake-case alias for :meth:`randomPolynomial`."""
        return Polynomial.randomPolynomial(degree, coef_min, coef_max, positive_leading)

    @staticmethod
    def from_coefficients(coefficients, variable='x', sort=True, simplify=True):
        """Build a polynomial from highest-degree-first coefficient list."""
        return Polynomial(coefficients, sort=sort, simplify=simplify, variable=variable)

    @staticmethod
    def from_roots(roots, leading_coefficient=1, variable='x'):
        """Build a monic (or scaled) polynomial from its roots."""
        product = Polynomial([leading_coefficient], variable=variable)
        for root in roots:
            product *= Polynomial([1, -root], variable=variable)
        return product

    @staticmethod
    def simplify_square_root(n):
        if n < 0:
            raise ValueError("radicand must be non-negative")
        if n == 0:
            return 0, 1

        coeff = 1
        radicand = int(n)
        factor = 2
        while factor * factor <= radicand:
            square = factor * factor
            while radicand % square == 0:
                radicand //= square
                coeff *= factor
            factor += 1 if factor == 2 else 2

        return coeff, radicand

    @staticmethod
    def square_root_latex(coeff, radicand):
        from .latex import square_root_latex
        return square_root_latex(coeff, radicand)

    @staticmethod
    def fraction_latex(numerator, denominator):
        from .latex import fraction_latex
        return fraction_latex(numerator, denominator)
    
    @staticmethod
    def createRationalAdditionProblemWithOneCancellation(leadingCoefficientRange,coefficientRange):
        '''
        

        Parameters
        ----------
        leadingCoefficientRange : Tuple
            length 2 tuple that represents range.
        coefficientRange : Tuple
            length 2 tuple that represents range.

        Returns
        -------
        coefficients of rational addition problem of the form
        
        a4x+b4 / a1x+b1 + a5x+b5 / a3x+b3
        
        
        a1a2=a3a4+a1a5
        
        (a1-b1)(a2-b2)=(a3-b3)(a4-b4)
        
        b1b2=b3b4+b1b5
        
        

        '''
        notGood = True
        
        while notGood:
            notGood=False
        
            aC= [float(random.randint(*leadingCoefficientRange)) for i in range(4)]
            
            aC.append((aC[0]*aC[1]-aC[2]*aC[3])/aC[0])        
            
            otherCheck=True
            
            while otherCheck:
                otherCheck=False
                bC= [float(random.randint(*coefficientRange)) for i in range(3)]
                otherCheck=aC[0]**2*bC[2]-aC[0]*bC[1]*aC[2]==0
            
            bC.append((aC[0]*bC[1]*aC[3]*bC[2]-bC[0]**2*aC[2]*aC[3])/(aC[0]**2*bC[2]-aC[0]*bC[1]*aC[2]))
            
            
            bC.append((bC[0]*bC[1]-bC[2]*bC[3])/bC[0])        
            
            
            fraction1= (Polynomial((aC[3],bC[3])),Polynomial((aC[0],bC[0])))
            
            fraction2= (Polynomial((aC[4],bC[4])),Polynomial((aC[2],bC[2])))
            
            for i in range(5):
                if aC[i]%1!=0.0 or bC[i]%1!=0.0:
                    notGood=True
            
                    
        
        
        return [aC,bC,fraction1,fraction2]
        
        
    
    @staticmethod 
    def checker(trials=100000,minDeg=3,maxDeg=30,minCoef=-100,maxCoef=100,tolerance=4,integer=True,output=False)  :
        count=0
        notify=100
        for i in range(trials) :
            if i%notify==0:
                print(str(i)+' of '+str(trials))
            
            if integer:
                p=Polynomial([random.randint(minCoef, maxCoef) for j in range(random.randint(minDeg+1, maxDeg+1))])
            else:
                p=Polynomial([(maxCoef-minCoef)*random.random()+minCoef for j in range(random.randint(minDeg, maxDeg+1))])
            x=Polynomial([1])
            a=p.factor()
            for po in a:
                x*=po
            if output or (not (round(x,tolerance)==round(p,tolerance))) :
                print("original:"+str(p.coef_list()),"\n attempt:"+str(x.coef_list()),"\n Factors: ")
                print('(',end='')
                print(*a,sep=')(',end='')
                print(')')
                count+=1
        return str(trials)+" trials completed with "+str(count)+" errors"
            
    
    
def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents



class Term:
    def __init__(self,variables={"":0}) :
        """
        

        Parameters
        ----------
        variables : Dictionary
            Dictionary of all variables
            Empty string is for coefficient

        Returns
        -------
        None.

        """



class SpecialPhrase:
    
    def __init__(self,phrase,valueFunction):
        '''
        

        Parameters
        ----------
        phrase : String
            the special phrase to look for
        valueFunction : Function with a return
            How to evaluate this phrase

        Returns
        -------
        None.

        '''
        self.phrase = phrase
        self.valueFunction = valueFunction
        self.arguements  = signature(valueFunction).parameters
    def evaluate(self,*values) :
        """
        

        Parameters
        ----------
        *values : Varies 
            The values required for the function

        Raises
        ------
        Exception
            If the given number of arguements is wrong

        Returns
        -------
        Varies
            The return from the valueFunction

        """
        
        if len(values)!=len(self.arguements):
            raise Exception("WRONG NUMBER OF ARGUEMENTS")
            
            
        
        vals = list(values) 
        
        for i in range(len(vals)):
            
            if type(vals[i])==list:
                raise Exception(str(vals[i])+" is a list")

            vals[i]=float(vals[i])
            
        
        return self.valueFunction(*vals)
    
    def __eq__(self, o):
        if type(o)==str:
            return self.phrase==o
        return None
    def __repr__(self):
        return self.phrase
    def __len__(self):
        return len(self.phrase)

class Expression:
    
    SPECIAL_OPERATIONS=3
    
    operations = [',','(',')','^','*','/','+','-']
    
    sin = SpecialPhrase("sin", lambda x: math.sin(x))
    
    cos = SpecialPhrase("cos", lambda x: math.cos(x))
    
    tan = SpecialPhrase('tan', lambda x: math.tan(x))
    
    arcsin = SpecialPhrase("arcsin", lambda x : math.asin(x))
    
    atan2 = SpecialPhrase('atan2', lambda x,y: math.atan2(y,x))

    specialPhrases = [sin,cos,tan,arcsin,atan2]
    
    
    def __init__(self,expression):
        self.expression=expression
  
    def evaluate(self) :
        

        return Expression.Evaluate(self.expression)[0]
    
    @staticmethod
    def commaSlicer(exp,commas) :
        #Chops it up into expressions around the commas
        
        def sliceHelper(exp,start,end):
            ret= []
            for i in range(start,end):
                ret.append(exp[i])
            return ret

        commaSeparatedExpressions = Expression.Evaluate(sliceHelper(exp,0,commas[0]))
        
        for i in range(1,len(commas)-1): 
            commaSeparatedExpressions+=Expression.Evaluate(sliceHelper(exp,commas[i]+1,commas[i+1]))

        commaSeparatedExpressions+=Expression.Evaluate(sliceHelper(exp,commas[-1]+1,len(exp)))
        
        return [tuple(commaSeparatedExpressions)]
        
        
    @staticmethod
    def Evaluate(string,commas=()):
        
        
        def functionNextToNonSpecialOpertaion(loc,parenValue):
            #checks if the function is not next to a basic operation
            if loc[0]-2>=0 and str(string[loc[0]-2]) not in Expression.operations[Expression.SPECIAL_OPERATIONS:]:
                parenValue=['*']+parenValue
            #will now get rid of specialphrase
            return ((loc[0]-1,loc[1]),parenValue)

        orderOfOperations = {0:"^",
                      1:"*/",
                      2:"+-"}
        
        if type(string)==str:
            string=Expression.tokenize(string)
        
        if len(commas)>0:
            return Expression.commaSlicer(string, commas)
        
        Expression.checkEqualNumberOfParen(string)
        #handle parenthesis
        if Expression.indexOf(string,'(')!=-1:
            (parenExpression,loc,commas)=Expression.findParenString(string)
            parenValue = Expression.Evaluate(parenExpression,commas=commas)
            
            #deal with parenthesis formatted for a multi-input function
            if type(parenValue[0])==tuple:
                if loc[0]==0 or Expression.indexOf(Expression.specialPhrases, str(string[loc[0]-1]))==-1:
                    raise Exception("Commas must be used for multi-input function")
                
                #Finds the appropriate specialphrase object
                specialPhrase = Expression.specialPhrases[Expression.indexOf(Expression.specialPhrases,str(string[loc[0]-1]))]
                parenValue = [specialPhrase.evaluate(*parenValue[0])]
                #will now get rid of specialphrase 
                loc,parenValue = functionNextToNonSpecialOpertaion(loc, parenValue)
                
            #deal with starting parenthesis not next to a basic operation
            elif loc[0]>0 and str(string[loc[0]-1]) not in Expression.operations[Expression.SPECIAL_OPERATIONS:]:
                
                #checks to see if the preceding token is a special phrase that takes arguements
                specialPhrase = Expression.indexOf(Expression.specialPhrases,str(string[loc[0]-1]))
                if specialPhrase==-1 or Expression.specialPhrases[specialPhrase].arguements==0:
                    parenValue=['*']+parenValue
                #deal with the parenthesis being for a single arguement function
                else:
                    parenValue= Expression.specialPhrases[specialPhrase].evaluate(parenValue[0])
                    #will now get rid of specialphrase
                    loc,parenValue = functionNextToNonSpecialOpertaion(loc, parenValue)
            #deal with ending parenthesis not next to basic operation
            if loc[1]<len(string)-1 and str(string[loc[1]+1]) not in Expression.operations[Expression.SPECIAL_OPERATIONS:]:
                ###TODO MAKE ALL OUTPUTS LISTS!!!
                
                
                
                parenValue+=['*']
            #replace the parenthesis expression with its value
            if type(parenValue)!=list:
                parenValue=[parenValue]
            
            simplified = string[0:loc[0]]+parenValue+string[loc[1]+1:]
            return Expression.Evaluate(simplified)
        
        levels=orderOfOperations.keys()
        #go through each operation level reading left to right
        for i in range (len(levels)):
            
            opsLeftAtLevel = True
            while opsLeftAtLevel:
                ops=orderOfOperations[i]
                minOp=-1
                #Finds the earliest operation of this level
                for op in ops:
                    nextOp = Expression.indexOf(string,op)
                    if nextOp!=-1:
                        minOp=nextOp if nextOp<minOp or minOp==-1 else minOp
                opsLeftAtLevel = minOp!=-1
                #If it found one, evaluate numbers of both sides
                if opsLeftAtLevel:
                    op=string[minOp]
                    #TODO make support for variable expressions
                    #probably by converting things into 
                    #term objects
                    leftVal=float(string[minOp-1])
                    rightVal=float(string[minOp+1])
                    
                    if op=='^':
                        val=leftVal**rightVal
                    elif op=='*':
                        val=leftVal*rightVal
                    elif op=='/':
                        val=leftVal/rightVal
                    elif op=='+':
                        val=leftVal+rightVal
                    elif op=='-':
                        val=leftVal-rightVal
                    else:
                        val=0
                    string.pop(minOp+1)
                    string.pop(minOp)
                    
                    string[minOp-1]=val

        return string
        
    
    @staticmethod 
    def checkEqualNumberOfParen(string):
        '''
        Checks if the number of open parens is unequal to close parens
        
        '''
        if string.count('(')!=string.count(')'):
            raise Exception("Unequal Parenthesis!")
            
    
    @staticmethod 
    def indexOf(lis, s, start=0,end=-1):
        '''
        Returns the first instance of s in a list lis

        Parameters
        ----------
        lis : list
            List to search for an element
        s : vaires
            Object to search for
        start : int, optional
            where to start search. The default is 0.
        end : int, optional
            where to end search. The default is -1.

        Returns
        -------
        int
            Index of first instance of s.

        '''
        if end==-1:
            end=len(lis)
        for i in range(start,end):
            if lis[i]==s:
                return i
        return -1
        
    @staticmethod
    def findParenString(string):
        
        
        
        '''
        Finds shallowest parenthesis in an expression
        will also return a tuple of all commas at this depth
        
        '''
        
        
        
        def findCommas(string) :
            """
            Returns the locations of commas in a string

            """
            ret=[]
            for (i,c) in enumerate(string) :
                if c==',':
                    ret.append(i)
            return ret
            
        
        start=string.index('(')
        end=string.index(')')
        
        commas = findCommas(string)
        
        

        if end==-1:
            raise Exception("Non-matching Parenthesis")
        checked=False
        prevParen = start
        while not checked :
            nextParen = Expression.indexOf(string,'(',prevParen+1,end)
            if nextParen>0:
                
                #Removes commas that are in a deeper parethesis
                for i in reversed(range(len(commas))) :
                    if commas[i]>nextParen and commas[i]<end:
                        commas.pop(i)
                
                
                end=Expression.indexOf(string,')',end+1)
                if end==-1:
                    raise Exception("Non-matching Parenthesis")
                prevParen=nextParen
            else:
                checked=True
        paren=string[start+1:end]
        
        if len(paren)==0:
            raise Exception("Empty Parenthesis")
            
        
        loc = (start,end)
        
        
            
        return (paren,loc,tuple(comma-start-1 for comma in commas))
        
    @staticmethod
    def tokenize(string) :
        
        
        
        def createSplitString(operationsAndSpecialPhrases):
            splitString = '(['
            
            for op in operationsAndSpecialPhrases:
                splitString+='\\'+op
            
            splitString+='])'
            return splitString
        
        
        def sliceList(exp, splitString,specialPhrasesToNotCut=None) :
            '''

            Parameters
            ----------
            exp : list or string
                The expression to be tokenized
            splitString : string
                The regular expression to split the string
             specialPhrasesToNotCut=None : string
                 Will avoid cutting these phrases into constituent parts

            Returns
            -------
            List
                A single list of all tokenized lists in order

            '''
            
            if type(exp) == list :
                ret=[]
                for e in exp:
                    ret+=sliceList(e,splitString,specialPhrasesToNotCut)
                    
                return ret
            
            if specialPhrasesToNotCut!=None:
                specialPhrasesToNotCut.sort(key=lambda s: len(s))
                
                #Take out all special phrases without chopping them up into letters
                #This will keep longer phrases with shorter phrases inside them
                
                for i in range(len(specialPhrasesToNotCut)):
                    
                    if str(specialPhrasesToNotCut[i]) in exp:
                        spec=specialPhrasesToNotCut[i]
                        foundLater= False
                        for j in range(i+1,len(specialPhrasesToNotCut)) :
                            if str(specialPhrasesToNotCut[j]) in exp:
                                foundLater=True
                        if not foundLater:
                            if len(exp)>len(spec):
                                
                                spec = '('+str(spec)+')'
                                
                                #print(sliceList(re.split(spec,exp),splitString,specialPhrasesToNotCut))
                                return sliceList(re.split(spec,exp),splitString,specialPhrasesToNotCut)
                            return [exp]
                        
            #print(list(filter(lambda s:s!="", re.split(splitString,exp))))
            return list(filter(lambda s:s!="", re.split(splitString,exp)))
        
        operationsAndSpecialPhrases=Expression.operations#+Expression.specialPhrases
        splitString=createSplitString(operationsAndSpecialPhrases)
        
        
        #splits based on operations, parenthesis, and special phrases
        tokenizedString = sliceList(string,splitString)
        
        
        
        #splits based on variables, keeping special phrases
        splitStringVariables = '([a-zA-Z])'
        
        
        
        
        tokenizedString = sliceList(tokenizedString,splitStringVariables,specialPhrasesToNotCut=Expression.specialPhrases)
        
        print(tokenizedString)

        return tokenizedString
            
        

class EquationViewer:
    def __init__(self,string):
        self.string=string
