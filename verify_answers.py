"""Independent check of the built-in sample bank's answer keys.

Every calculation-based question in questions.js is recomputed here from
first principles (SymPy / plain arithmetic) and compared with the answer key
stored in questions.js. Conceptual questions (facts such as molecular shapes
or reaction products) cannot be computed and are listed for manual review.

Usage:  pip install sympy && python3 verify_answers.py   (needs Node.js)
"""
import json, subprocess, sys
from itertools import permutations
from math import comb, sqrt as s, pi as PI
from sympy import *

bank = json.loads(subprocess.check_output(
    ["node", "-e", "global.window={};require('./questions.js');console.log(JSON.stringify(window.JEE_SAMPLE_BANK))"]))
Q = {q["id"]: q for q in bank}
def key(i):
    q = Q[i]
    return q["answer"] if q["type"] == "NUM" else q["options"][q["answer"]]

x = symbols('x'); chk = []
def c(id, got, exp):
    """Record whether the independent result 'got' equals the expected value 'exp'."""
    chk.append((id, abs(float(got) - float(exp)) < 1e-6, got, exp))
def c(id,got,exp): chk.append((id, abs(float(got)-float(exp))<1e-6, got, exp))
c('P02',3*1+2*3+0.5*4+2,13); c('P03',400*0.25/20,5); c('P04',4*(2*5-1)/2,18)
c('P05',3*(10/5),6); c('P06',min(15,0.4*5*10),15); c('P07',(0.5*2*100)/5,20)
c('P08',600*10*10/60,1000); c('P09',Rational(1,12)+Rational(1,4),Rational(1,3))
c('P10',Rational(1,5)/Rational(7,10),Rational(2,7)); c('P11',2*11.2,22.4)
h=symbols('h',positive=True); c('P12',solve(Eq(1/(1+h)**2,Rational(1,4)),h)[0],1)
c('P13',1-400/800,0.5); c('P14',2*1.5*8.3*100,2490); c('P15',2*s(1.44),2.4)
c('P16',100*2,200); xs=solve(Eq(1/x**2,4/(1-x)**2),x); c('P17',[v for v in xs if 0<v<1][0],Rational(1,3))
c('P18',0.5*5e-6*100**2*1e3,25); c('P19',8*8/16,4); c('P20',12-1*12/6,10)
c('P21',(1/1)/(4/2),0.5); c('P22',4*PI*1e-7*100*1/(2*0.1),6.283185307e-4)
c('P23',1/s(10e-3*1e-6),1e4); c('P24',0.5*4/0.1,20)
c('P25',1/(1/-20.0-1/-30.0),-60); c('P26',1/sin(pi/6),2); c('P27',5-2,3); c('P28',1600/2**4,100)
c('C01',9.8/98*4,0.4); c('C02',2*0.25*50/0.5,50); c('C03',3-1-1,1)
c('C07',40000/100,400); c('C08',-(-393+2*-286+75),890); c('C10',14+log(0.001,10),11)
c('C11',(14-2)/2,6); c('C12',round(2*96500*1.1/1000),212); c('C13',30*log(4)/log(2),60)
c('C14',2*2**2,8); c('C16',0.5*(18/180)*100,5); c('C19',s(5*7),5.916079783)
def canon(p):
    rots=[p[i:]+p[:i] for i in range(4)]; rots+=[r[::-1] for r in rots]; return min(rots)
c('C22',len({canon(''.join(p)) for p in permutations('abcd')}),3)
c('M01',2**(9-3),64); c('M03',simplify(((1+I)/(1-I))**100),1)
c('M04',Abs((3+4*I)*(5-12*I)),65); c('M05',5**2-2*6,13)
c('M06',len([r for r in range(-10,11) if r*r-5*abs(r)+6==0]),4)
A=Matrix([[2,3],[1,2]]); c('M07',4**2,16); chk.append(('M08',A.inv()==Matrix([[2,-3],[-1,2]]),A.inv(),''))
c('M09',factorial(5)/(2*2),30); c('M10',comb(6,3)*comb(5,2),200); c('M11',comb(10,4),210); c('M12',comb(8,4),70)
c('M13',1/(1-Rational(1,3)),Rational(3,2)); c('M14',4+9*4,40)
c('M15',limit(sin(3*x)/x,x,0),3); c('M16',limit((exp(x)-1-x)/x**2,x,0),Rational(1,2))
f=x**3-3*x+2; cp=solve(diff(f,x),x); mx=[p for p in cp if diff(f,x,2).subs(x,p)<0][0]; c('M17',f.subs(x,mx),4)
c('M18',diff(x**3-2*x+1,x).subs(x,2),10)
c('M19',integrate(sin(x)**2,(x,0,pi/2)),pi/4); c('M20',integrate(3*x**2+2*x,(x,0,2)),12)
c('M23',abs(-7-3)/5,2); c('M24',s(1-16/25),0.6); c('M25',4*3,12); c('M26',1*2+2*-1+3*1,3)
c('M27',abs(2*1-2+2*3+3)/3,3); c('M28',Rational(sum(1 for a in range(1,7) for b in range(1,7) if a+b==7),36),Rational(1,6))

# Cross-check: the expected values above must match what questions.js actually keys.
KEYED = {"P02":"13%","P03":"5 m","P04":18,"P05":"6 N","P06":"15 N","P07":"20 N","P08":1000,"P09":"ML²/3",
 "P10":"2/7","P11":"22.4 km/s","P12":"R","P13":"50%","P14":2490,"P15":"2.4 s","P16":"200 m/s","P17":"d/3",
 "P18":25,"P19":"4 Ω","P20":"10 V","P21":"1 : 2","P22":"6.28 × 10⁻⁴ T","P23":"10⁴ rad/s","P24":20,
 "P25":"60 cm in front of the mirror","P26":"2","P27":"3 V","P28":100,"C01":"0.4","C02":50,"C03":"1",
 "C07":"400 K","C08":890,"C10":"11","C11":"+6","C12":212,"C13":"60 min","C14":"8","C16":5,"C19":"5.92 BM",
 "C22":3,"M01":"64","M03":"1","M04":65,"M05":"13","M06":4,"M07":"16","M08":"[2 −3 ; −1 2]","M09":"30",
 "M10":200,"M11":"210","M12":"70","M13":"3/2","M14":40,"M15":"3","M16":"1/2","M17":"4","M18":"10",
 "M19":"π/4","M20":12,"M23":"2","M24":"3/5","M25":12,"M26":"3","M27":3,"M28":"1/6"}
mismatch = [(i, key(i), v) for i, v in KEYED.items() if key(i) != v]
bad = [k for k in chk if not k[1]]
manual = sorted(set(Q) - set(KEYED))
print(f"{len(chk)} computed checks, {len(bad)} failed: {bad}")
print(f"{len(KEYED)} answer keys cross-checked, {len(mismatch)} mismatched: {mismatch}")
print(f"Conceptual questions for manual review ({len(manual)}):", ", ".join(manual))
sys.exit(1 if bad or mismatch else 0)
