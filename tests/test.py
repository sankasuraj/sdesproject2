from kriging import *
import unittest
import numpy.testing as npt
import pytest
import os


def generate_test_data(num_rows, num_columns):
    global x_test
    global y_test
    x_test = []
    y_test = []
    for i in range(num_rows):
        x_test.append(np.random.normal(0.0, 100.0, num_columns))
        y_test.append([np.random.uniform(0.0, 100.0)])
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    global model_test
    model_test = Solve(x_test, y_test)


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
        for i in range(model_test.n):
            for j in range(model_test.k):
                assert 0.0 <= model.x_test[i][j] <= 1.0

    def test_for_normalisation_y(self):
        for i in range(model_test.n):
            assert 0.0 <= model_test.y_test[i] <= 1.0

    def test_for_inverse_normalisation_y(self):
        self.compare_arrays(model_test.inversenormy(model_test.y), y_test)

    def test_for_inverse_normalisation_x(self):
        for i in range(model_test.k):
            given = (
                model_test.x[:, i] * (model_test.max_x[i] -
                                      model_test.min_x[i]) + model_test.min_x[i])
            self.compare_arrays(given, x_test[:, i])

    def test_for_training(self):
        f = open('test.csv', 'wb')
        writer = csv.writer(f, delimiter=',')
        for i in range(model_test.n):
            row = np.concatenate([x_test[i], y_test[i]])
            writer.writerow(row)
        f.close()
        assert os.path.exists('test.csv')
        train_model('model.csv', 'test.csv')
        assert os.path.exists('model.csv')
        os.remove('test.csv')
        os.remove('model.csv')


if __name__ == '__main__':
    unittest.main()
