from numpy.random import multivariate_normal

class GaussianTrashSource:

        def __init__(self, coords, cov, id, ):
            # mean of the gaussian
            self.coords = coords
            # covariance matrix of the multivariate gaussian
            self.cov = cov

        def draw_sample():
            x,y = multivariate_normal(coords,cov,1)
            return (y,x)

        def get_trash():
            return draw_sample()

        def get_trash(n):
            """
                Returns a list of n coordinates drawn from the distribution
            """
            return [get_trash() for i in range(n)]
