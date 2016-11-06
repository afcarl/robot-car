from utils.matrix import matrix 

def filter(x, P):
    for n in range(len(measurements)):
        
        # prediction
        x = (F * x) + u
        P = F * P * F.transpose()
        
        # measurement update
        Z = matrix([measurements[n]])
        y = Z.transpose() - (H * x)
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + (K * y)
        P = (I - (K * H)) * P
    
    print 'x= '
    x.show()
    print 'P= '
    P.show()

########################################


measurements = [[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]]
initial_xy = [4., 12.]

dt = 0.1

x = matrix([[initial_xy[0]], [initial_xy[1]], [0.], [0.]]) # initial state (location and velocity)
u = matrix([[0.], [0.], [0.], [0.]]) # external motion

# Note: since initial x,y is given, the uncertainty is 0, only verlocity uncertainty is high
# initial uncertainty
P =  matrix([[0, 0., 0., 0.], 
			 [0., 0, 0., 0.], 
			 [0., 0., 1000., 0.], 
			 [0., 0., 0., 1000]]) 

# next state function
F =  matrix([[1., 0., dt, 0.], 
			 [0., 1., 0., dt], 
			 [0., 0., 1., 0.], 
			 [0., 0., 0., 1.]])

# measurement function
H =  matrix([[1., 0., 0., 0.], 
			 [0., 1., 0., 0.]]) 

# measurement uncertainty
R =  matrix([[0.1, 0.], 
			 [0., 0.1]]) 

#identity matrix
I =  matrix([[1., 0., 0., 0.],
			 [0., 1., 0., 0.], 
			 [0., 0., 1., 0.], 
			 [0., 0., 0., 1.]]) 

if __name__ == "__main__":
	print "### 4-dimensional example ###"
	filter(x,P)
