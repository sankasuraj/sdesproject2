from kriging import *

def generate_test_data():
	x = []
	y = []
	n = np.random.randint(10) + 2
	for i in range(100):
		x.append(np.random.normal(0.0, 100.0, n))
		y.append([np.random.uniform(0.0, 100.0)])
	return np.array(x), np.array(y)

def test_for_normalisation():
	x, y = generate_test_data()
	model = Solve(x, y)