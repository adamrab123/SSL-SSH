import secrets


# this is assuming the curve is given by y^2 = x^3 + ax + b
def ECC_add(Xp,Yp,Xq,Yq,a):
    if Xp == Xq and Yp == Yq:
        Lambda = 3*(Xp**2) + a / (2 * Yp)
    else:
        Lambda = (Yq-Yp)/(Xq-Xp)
    Xr = Lambda**2 - Xp - Xq
    Yr = Lambda*(Xp-Xr)-Yp
    return [Xr,Yr]

# n = 128

a,b = 10,7


#######################################
#ALICE CREATING PRIVATE AND PUBLIC KEYS
#######################################
GA = [3,8]

d1 = secrets.randbelow(10)
#ensuring it isn't 0
while d1 == 0:
    d1 = secrets.randbelow(10)
print(d1)

QAx,QAy = GA

print(QAx,QAy)

for i in range(d1):
    QAx,QAy = ECC_add(QAx,QAy,GA[0],GA[1],a)

print(QAx, QAy)

#######################################
#BOB CREATING PRIVATE  AND  PUBLIC KEYS
#######################################

GB = GA
# print("GB =", GB)

d2 = secrets.randbelow(10)
#ensuring it isn't 0
while d2 == 0:
    d2 = secrets.randbelow(10)
print(d2)

QBx,QBy = GB

print(QBx,QBy)

for i in range(d2):
    QBx,QBy = ECC_add(QBx,QBy,GB[0],GB[1],a)

print(QBx, QBy)

#######################################
#COMPUTING         SHARED          KEY
#######################################

Axk, Ayk = QBx, QBy
for i in range(d1):
    Axk, Ayk = ECC_add(Axk,Ayk,QBx, QBy,a)
print(Axk,Ayk)

Bxk, Byk = QAx, QAy
for i in range(d2):
    Bxk, Byk = ECC_add(Bxk,Byk,QAx, QAy,a)
print(Bxk,Byk)

#this should print two lines of true once is starts working
print(Axk==Bxk)
print(Ayk==Byk)

# y^{2}=x^{3}+ax+b
# Domain Parameters
# p - prime
# a - a(x) term
# b - +b term
# G - cyclic subgroup generator
# n - size of the subgroup
# h - cofactor; meant to be small (<=4, preferably 1)
