from kriging import *
import mock
import unittest
import numpy.testing as npt

def generate_test_data(num_rows, num_columns):
	global x 
	global y
	x = []
	y = []
	for i in range(num_rows):
		x.append(np.random.normal(0.0, 100.0, num_columns))
		y.append([np.random.uniform(0.0, 100.0)])
	x = np.array(x)
	y = np.array(y)
	global model 
	model = Solve(x, y)



class TestKriging(unittest.TestCase):

	def setUp(self):
		generate_test_data(4, 20)

	def tearDown(self):
		ok = self.currentResult.wasSuccessful()
		errors = self.currentResult.errors
		failures = self.currentResult.failures
		if ok:
			print ' All tests passed so far!'
		else:
			'%d errors and %d failures so far' % (len(errors), len(failures))

	def assert_error(self, given, expected, precision):
		return npt.assert_almost_equal(given, expected, precision)

	def run(self, result=None):
		self.currentResult = result
		unittest.TestCase.run(self, result)

	def test_for_normalisation_x(self):
		for i in range(model.n):
			for j in range(model.k):
				assert 0.0 <= model.x[i][j] <= 1.0

	def test_for_normalisation_y(self):
		for i in range(model.n):
			assert 0.0 <= model.y[i] <= 1.0

	def test_for_inverse_normalisation_y(self):
		self.assert_error(model.inversenormy(model.y), y, 8)			

	def test_for_inverse_normalisation_x(self):
		for i in  range(model.k):
			given = model.x[:,i] * (model.max_x[i] - model.min_x[i]) + model.min_x[i]
			self.assert_error(given, x[:,i], 8)

if __name__ == '__main__':
	unittest.main()