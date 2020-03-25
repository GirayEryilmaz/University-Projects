import numpy as np
from scipy import stats


class Zipf:
	def getZipf(self):
		N = 100
		x = np.arange(1, N + 1)
		a = 1.0
		weights = x ** (-a)
		weights /= weights.sum()
		bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))
		
		sample = bounded_zipf.rvs(size=100)
		# print(sample)
		
		return sample
