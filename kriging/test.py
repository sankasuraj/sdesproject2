from kriging import *
import mock
import unittest
import numpy.testing as npt
import pytest
import os

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
		generate_test_data(20, 4)

	def tearDown(self):
		ok = self.currentResult.wasSuccessful()
		errors = self.currentResult.errors
		failures = self.currentResult.failures
		if ok:
			print ' All tests passed so far!'
		else:
			'%d errors and %d failures so far' % (len(errors), len(failures))

	def compare_arrays(self, array1, array2):
		for i in range(len(array1)):
			assert array1[i] == pytest.approx(array2[i])

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
		self.compare_arrays(model.inversenormy(model.y), y)

	def test_for_inverse_normalisation_x(self):
		for i in  range(model.k):
			given = model.x[:,i] * (model.max_x[i] - model.min_x[i]) + model.min_x[i]
			self.compare_arrays(given, x[:,i])

	# @mock.patch('builtins.open', mock_open)
	# def test_for_training(self, mock_open()):
	# 	f = open('test.csv', 'wb')
	# 	writer = csv.writer(f, delimiter=',')
	# 	for i in range(model.n):
	# 		row = np.concatenate([x[i], y[i]])
	# 		writer.writerow(row)
	# 	f.close()
	# 	self.assertEqual(os.path.exists.received_args[0], 'test.csv')
 #        mock_open().assert_called_once_with('test.csv', 'w+')
	# 	# model.train_model('model.csv')


if __name__ == '__main__':
	unittest.main()