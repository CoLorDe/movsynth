import numpy as np

#TODO add inquirer to select functions

class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, x=float, y=float):
        self.X = x
        self.Y = y

    def __str__(self):
        return "Point(%s, %s)"%(self.X, self.Y)

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y)

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return np.sqrt(dx**2 + dy**2)

    @classmethod
    def user_input(self):
        while 1:
            try:
                x = input('Enter x: ')
                x = float(x)
                y = input('Enter y: ')
                y = float(y)
                return self(x, y)
            except:
                print('Invalid input!')
                continue

def quad_synth():
    print("This function finds the distance between the hinges of a four-bar linkage, given 2 fixed hinges and 3 passage positions relative to the coupler(floating link).")
    h1 = Point(0, 0)
    print("Insert the second fixed hinge coordinates(first hinge is at (0, 0))")
    h2 = Point.user_input()


    print("Insert the first passage point coordinates")
    m1 = Point.user_input()
    print("Insert the second passage point coordinates")
    m2 = Point.user_input()
    print("Insert the third passage point coordinates")
    m3 = Point.user_input()




    counter = 0
    for i in range(0, 180):
        theta1=np.radians(i)
        for j in range(0,180):
            theta2 = np.radians(j)
            if(j>i+5):
                sin1 = np.sin(theta1)
                cos1 = np.cos(theta1)
                sin2 = np.sin(theta2)
                cos2 = np.cos(theta2)

                #rotations of m1 to m2 and m3
                t2 = m2.X - m1.X * cos1 + m1.Y * sin1
                s2 = m2.Y - m1.X * sin1 - m1.Y * cos1
                t3 = m3.X - m1.X * cos2 + m1.Y * sin2
                s3 = m3.Y - m1.X * sin2 - m1.Y * cos2

                #first fixed hinge equations
                a2 = t2*cos1+s2*sin1
                b2 = s2*cos1-t2*sin1
                c2 = -(t2*t2+s2*s2)/2

                a3 = t3*cos2+s3*sin2
                b3 = s3*cos2-t3*sin2
                c3 = -(t3*t3+s3*s3)/2

                #second fixed hinge equations
                d2 = t2*cos1+s2*sin1-h2.X*cos1-h2.Y*sin1+h2.X
                e2 = s2*cos1-t2*sin1+h2.X*sin1-h2.Y*cos1+h2.Y
                f2 = t2*h2.X+s2*h2.Y-(t2*t2+s2*s2)/2

                d3 = t3*cos2+s3*sin2-h2.X*cos2-h2.Y*sin2+h2.X
                e3 = s3*cos2-t3*sin2+h2.X*sin2-h2.Y*cos2+h2.Y
                f3 = t3*h2.X+s3*h2.Y-(t3*t3+s3*s3)/2

                #calculate coordinates of the first mobile hinge
                y1=(c3*a2-a3*c2)/(a2*b3-a3*b2)
                x1=(c3*b2-b3*c2)/(a3*b2-a2*b3)

                #calculate coordinates of the second mobile hinge
                y2=(f3*d2-d3*f2)/(d2*e3-d3*e2)
                x2=(f3*e2-e3*f2)/(d3*e2-d2*e3)

                #create hinges points
                a = Point(x1, y1)
                b = Point(x2, y2)

                #calculate distance between hinges
                r1 = h1.distance(a)
                r2 = a.distance(b)
                r3 = b.distance(h2)
                r4 = h2.distance(h1)

                #check if one bar can rotate continuously, Grashof criterion
                grashof = False
                if (r1<r4 and r1<r2 and r1<r3):
                    if (r4>r3 and r4>r2):
                        if ((r1+r4)<=(r2+r3)):
                            grashof = True
                    else:
                        if (r3>r4 and r3>r2):
                            if ((r1+r3)<=(r2+r4)):
                                grashof = True
                            else:
                                if ((r1+r2)<=(r3+r4)):
                                    grashof= True


                if grashof:
                    #check max and min transimsission angle, through "Law of cosines"
                    #this is to avoid low transimsission
                    maxangle = np.degrees(np.arccos((r3**2+r2**2-(r4+r1)**2)/(2*r3*r2)))
                    minangle = np.degrees(np.arccos((r3**2+r2**2-(r4-r1)**2)/(2*r3*r2)))


                    if (minangle>50 and maxangle<130):
                        print("Configurazione trovata \n"+h1.__str__()+"\n"+h2.__str__()+"\n"+a.__str__()+"\n"+b.__str__()+"\n")
                        print(r1,r2,r3,r4)
                        counter+=1

    print("\n")
    print("Number of four bars found: %s" % (counter))

quad_synth()
