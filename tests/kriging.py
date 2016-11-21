import csv
import numpy as np
import copy
import inspyred
from random import Random
from time import time
from inspyred import ec
import scipy
from scipy.optimize import minimize
import math as m


class Solve:

    def __init__(self, x, y):
        self.LnDetPsi = None
        self.SigmaSqr = None
        self.x = copy.deepcopy(x)
        self.y = copy.deepcopy(y)
        self.n = self.x.shape[0]
        self.k = self.x.shape[1]
        self.theta = np.ones(self.k)
        self.pl = np.ones(self.k) * 2.0
        self.max_x = None
        self.min_x = None
        self.max_y = max(y)
        self.min_y = min(y)
        self.normalizeData()
        self.Psi = np.zeros((self.n, self.n), dtype=np.float)
        self.psi = np.zeros((self.n, 1))
        self.one = np.ones(self.n)
        self.mu = None
        self.U = None
        self.distance = None
        self.updateData()
        self.thetamin = 1e-5
        self.thetamax = 100
        self.pmin = 1
        self.pmax = 2

    def normx(self, x):
        normalised = []
        for i in range(self.k):
            normalised.append((x[i] - self.min_x[i]) /
                              (self.max_x[i] - self.min_x[i]))
        return np.array(normalised)

    def normy(self, y):
        return (y - self.min_y) / (self.max_y - self.min_y)

    def inversenormy(self, normy):
        return normy * (self.max_y - self.min_y) + self.min_y

    def normalizeData(self):
        max_x = []
        min_x = []
        for i in range(self.k):
            max_x.append(max(self.x[:, i]))
            min_x.append(min(self.x[:, i]))
        self.max_x = np.array(max_x)
        self.min_x = np.array(min_x)
        for i in range(self.n):
            self.x[i] = self.normx(self.x[i])
            self.y[i] = self.normy(self.y[i])

    def updateData(self):
        self.distance = np.zeros((self.n, self.n, self.k))
        for i in xrange(self.n):
            for j in xrange(i + 1, self.n):
                self.distance[i, j] = np.abs((self.x[i] - self.x[j]))
        newPsi = np.exp(-np.sum(self.theta *
                                np.power(self.distance, self.pl), axis=2))
        self.Psi = np.triu(newPsi, 1)
        self.Psi = self.Psi + self.Psi.T + np.eye(self.n) + np.eye(self.n)
        self.U = np.linalg.cholesky(self.Psi)
        self.U = np.matrix(self.U.T)
        a = np.linalg.solve(self.U.T, self.one)
        b = np.linalg.solve(self.U, a)
        c = self.one.T.dot(b)
        d = np.linalg.solve(self.U.T, self.y)
        e = np.linalg.solve(self.U, d)
        self.mu = (self.one.T.dot(e)) / c

    def generate_population(self, random, args):
        '''
        Generates an initial population for any global optimization that occurs
        in pyKriging
        :param random: A random seed
        :param args: Args from the optimizer, like population size
        :return chromosome: The new generation for our global optimizer to use
        '''
        size = args.get('num_inputs', None)
        bounder = args["_ec"].bounder
        chromosome = []
        for lo, hi in zip(bounder.lower_bound, bounder.upper_bound):
            chromosome.append(random.uniform(lo, hi))
        return chromosome

    def no_improvement_termination(self, population, num_generations,
                                   num_evaluations, args):
        """Return True if the best fitness does not change for a number of
        generations of if the max number
        of evaluations is exceeded.

        .. Arguments:
                population -- the population of Individuals
                num_generations -- the number of elapsed generations
                num_evaluations -- the number of candidate solution evaluations
                args -- a dictionary of keyword arguments

        Optional keyword arguments in args:

        - *max_generations* -- the number of generations allowed for no change
        in fitness (default 10)

        """
        max_generations = args.setdefault('max_generations', 10)
        previous_best = args.setdefault('previous_best', None)
        max_evaluations = args.setdefault('max_evaluations', 30000)
        current_best = np.around(max(population).fitness, decimals=4)
        if previous_best is None or previous_best != current_best:
            args['previous_best'] = current_best
            args['generation_count'] = 0
            return False or (num_evaluations >= max_evaluations)
        else:
            if args['generation_count'] >= max_generations:
                return True
            else:
                args['generation_count'] += 1
                return False or (num_evaluations >= max_evaluations)

    def neglikelihood(self):
        self.LnDetPsi = 2.0 * np.sum(np.log(np.abs(np.diag(self.U))))
        a = np.linalg.solve(self.U.T, self.one.T)
        b = np.linalg.solve(self.U, a)
        c = self.one.T.dot(b)
        d = np.linalg.solve(self.U.T, self.y)
        e = np.linalg.solve(self.U, d)
        self.mu = (self.one.T.dot(e)) / c
        temp = np.linalg.solve(self.U.T, (self.y - self.mu))
        self.SigmaSqr = (
            (self.y - self.mu).T.dot(np.linalg.solve(self.U, temp))) / self.n
        self.NegLnLike = -1. * \
            (-(self.n / 2.) * np.log(self.SigmaSqr) - 0.5 * self.LnDetPsi)

    regneglikelihood = neglikelihood

    def fittingObjective(self, candidates, args):
        '''
        The objective for a series of candidates from the hyperparameter global
        search.
        :param candidates: An array of candidate design vectors from the global
        optimizer
        :param args: args from the optimizer
        :return fitness: An array of evaluated NegLNLike values for the
        candidate population
        '''
        fitness = []
        for entry in candidates:
            f = 10000
            for i in range(self.k):
                self.theta[i] = entry[i]
            for i in range(self.k):
                self.pl[i] = entry[i + self.k]
            self.neglikelihood()
            f = self.NegLnLike
            fitness.append(f)
        return fitness

    def fittingObjective_local(self, entry):
        '''
        :param entry: The same objective function as the global optimizer,but
        ormatted for the
         local optimizer
        :return: The fitness of the surface at the hyperparameters specified in
        entry
        '''
        f = 10000
        for i in range(self.k):
            self.theta[i] = entry[i]
        for i in range(self.k):
            self.pl[i] = entry[i + self.k]
        self.neglikelihood()
        f = self.NegLnLike
        return f

    def train(self):
        '''
        The function trains the hyperparameters of the Kriging model.
        :param optimizer: Two optimizers are implemented, a Particle Swarm
        Optimizer or a GA
        '''

        self.updateData()

        lowerBound = [self.thetamin] * self.k + [self.pmin] * self.k
        upperBound = [self.thetamax] * self.k + [self.pmax] * self.k

        # Create a random seed for our optimizer to use
        rand = Random()
        rand.seed(int(time()))

        ea = inspyred.swarm.PSO(Random())
        ea.terminator = self.no_improvement_termination
        ea.topology = inspyred.swarm.topologies.ring_topology
        final_pop = ea.evolve(
         generator=self.generate_population, evaluator=self.fittingObjective,
         pop_size=300, maximize=False,
         bounder=ec.Bounder(lowerBound, upperBound),
         max_evaluations=30000, neighborhood_size=20, num_inputs=self.k
         )
        final_pop.sort(reverse=True)

        for entry in final_pop:
            newValues = entry.candidate
            preLOP = copy.deepcopy(newValues)
            locOP_bounds = []
            for i in range(self.k):
                locOP_bounds.append([self.thetamin, self.thetamax])

            for i in range(self.k):
                locOP_bounds.append([self.pmin, self.pmax])

            lopResults = minimize(
             self.fittingObjective_local, newValues, method='SLSQP',
             bounds=locOP_bounds, options={'disp': False}
             )

            newValues = lopResults['x']

            for i in range(self.k):
                self.theta[i] = newValues[i]
            for i in range(self.k):
                self.pl[i] = newValues[i + self.k]

    def predict_normalized(self, x):
        for i in range(self.n):
            self.psi[i] = np.exp(-np.sum(self.theta *
                                         np.power((
                                           np.abs(self.x[i] - x)), self.pl)))
        z = self.y - self.mu
        a = np.linalg.solve(self.U.T, z)
        b = np.linalg.solve(self.U, a)
        c = self.psi.T.dot(b)
        f = self.mu + c
        return f[0]

    def predict(self, x):
        self.updateData()
        normx = self.normx(x)
        normy = self.predict_normalized(normx)
        return self.inversenormy(normy)


def str_to_float(row):
    result = []
    for char in row:
        result.append(float(char))
    return np.array(result)


def read_data(file_name):
    f = open(file_name, 'rb')
    data = csv.reader(f, delimiter=',')
    x = []
    y = []
    for row in data:
        x.append(str_to_float(row[:-1]))
        rowy = [float(row[-1])]
        y.append(np.array(rowy))
    f.close()
    return np.array(x), np.array(y)


def divide_data(x, y):
    length = x.shape[0]
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in range(1, length + 1):
        if i % 5 == 0:
            x2.append(x[i - 1])
            y2.append(y[i - 1])
        else:
            x1.append(x[i - 1])
            y1.append(y[i - 1])
    return np.array(x1), np.array(y1), np.array(x2), np.array(y2)


def estimate_error(model, x, y):
    estimate_y = []
    for row in x:
        estimate_y.append(model.predict(row))
    estimate_y = np.array(estimate_y)
    error = np.sqrt(sum(np.ravel(estimate_y - y) *
                        np.ravel(estimate_y - y))) / len(y)
    return error


def train_model(model_name, training_data_file):
    start = time()
    x, y = read_data(training_data_file)
    x1, y1, x2, y2 = divide_data(x, y)
    print 'Preliminary model initialising...'
    prelim_model = Solve(x1, y1)
    print 'Preliminary model initialised'
    print 'Preliminary model training started'
    prelim_model.train()
    print 'Preliminary model trained'

    print 'Estimating error using preliminary model'
    error = estimate_error(prelim_model, x2, y2)
    print 'Error estimation done'

    print 'Final model initialising...'
    final_model = Solve(x, y)
    print 'Final model initialised'
    print 'Final model training started'
    print 'Esimated time remaining is approximately ' + str(int(1.45 * (time() - start))) + ' seconds'
    final_model.train()
    print 'Final model trained'

    end = time()
    print 'Total time taken = ' + str(int(end - start)) + ' seconds'
    print 'L2 error for the given data = ' + str(round(error, 2))

    f = open(model_name, 'wb')
    writer = csv.writer(f, delimiter=',')
    writer.writerow(np.concatenate([final_model.max_x, final_model.max_y]))
    writer.writerow(np.concatenate([final_model.min_x, final_model.min_y]))
    for i in range(final_model.n):
        writer.writerow(x[i])
    f.close()


def find_values(model_name, find_y, outname):
    model_file = open(model_name, 'rb')
    model_data = csv.reader(model_file, delimiter=',')
    n = 0
    normalised_x = []
    for row in model_data:
        if n == 0:
            x_max = str_to_float(row[:-1])
            y_max = float(row[-1])
        elif n == 1:
            x_min = str_to_float(row[:-1])
            y_min = float(row[-1])
        else:
            normalised_x.append(str_to_float(row))
        n += 1
    normalised_x = np.array(normalised_x)
    model_file.close()
    print 'Model loaded'
    model = Solve(normalised_x, normalised_x[:, 0])
    model.max_x = np.array(x_max)
    model.min_x = np.array(x_min)
    model.max_y = y_max
    model.min_y = y_min
    model.updateData()
    print 'Estimation started'
    estimation_file = open(find_y, 'rb')
    x_data = csv.reader(estimation_file, delimiter=',')
    x = []
    for row in x_data:
        x.append(str_to_float(row))
    estimation_file.close()
    estimate_y = []
    for row in x:
        estimate_y.append(model.predict(row))
    print 'Estimation done'
    outfile = open(outname, 'wb')
    writer = csv.writer(outfile, delimiter=',')
    for row in estimate_y:
        writer.writerow([row])
    outfile.close()
    print 'Outfile written'
