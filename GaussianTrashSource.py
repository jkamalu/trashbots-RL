from numpy.random import multivariate_normal

class GaussianTrashSource:

        def __init__(self, mean, max_y, max_x, cov=None, id=None):
            """
            Creates a trashsource

            Parameters
            ----------
            cov: 2x2 matrix, covariance of the rnd var.
            coords: (int,int), (y,x) trash hotspot, mean of the rnd var.
            max_x : int, limits to the trash coordinates / grid of the environment
            max_y : int, limits to the trash coordinates / grid of the environment

            Returns
            -------
            """
            # mean of the gaussian
            self.mean = mean
            # covariance matrix of the multivariate gaussian
            if cov==None:
                cov = [[1,0],
                        [0,1]]
            self.cov = cov

            # strict limits to the gaussian
            self.max_x = max_x
            self.max_y = max_y

            # Just an id of the trashsource
            self.id = id


        def draw_sample_in_limits(self):
            """

            """
            y, x = multivariate_normal(self.mean, self.cov,1)[0]
            y = min(self.max_y, round(y))
            x = min(self.max_x, round(x))

            return [y, x]

        def get_trash(self, n=None):
            """
            Returns a list of n coordinates drawn from the distribution
            """

            if n:
                return [self.draw_sample_in_limits() for i in range(n)]
            return self.draw_sample_in_limits()
