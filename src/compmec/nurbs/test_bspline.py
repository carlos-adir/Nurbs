import unittest
import Bspline as SBF
import numpy as np


class TestSplineBaseFunction(unittest.TestCase):

    def test_CreationClass(self):
        SBF.SplineBaseFunction([0, 0, 1, 1])
        SBF.SplineBaseFunction([0, 0, 0, 1, 1, 1])
        SBF.SplineBaseFunction([0, 0, 0, 0, 1, 1, 1, 1])
        SBF.SplineBaseFunction([0, 0, 0, 0, 0.5, 1, 1, 1, 1])

        with self.assertRaises(TypeError):
            SBF.SplineBaseFunction(-1)
            SBF.SplineBaseFunction({1: 1})

        with self.assertRaises(ValueError):
            SBF.SplineBaseFunction([0, 0, 0, 1, 1])
            SBF.SplineBaseFunction([0, 0, 1, 1, 1, ])
            SBF.SplineBaseFunction([0, 0, 0, 0, 1, 1, 1])
            SBF.SplineBaseFunction([0, 0, 0, 1, 1, 1, 1])
            SBF.SplineBaseFunction([-1, -1, 1, 1])
            SBF.SplineBaseFunction([0, 0, 2, 2])

    def test_ValuesOfP(self):
        N = SBF.SplineBaseFunction([0, 0, 1, 1])
        self.assertEqual(N.p, 1)
        N = SBF.SplineBaseFunction([0, 0, 0, 1, 1, 1])
        self.assertEqual(N.p, 2)
        N = SBF.SplineBaseFunction([0, 0, 0, 0, 1, 1, 1, 1])
        self.assertEqual(N.p, 3)

        N = SBF.SplineBaseFunction([0, 0, 0.5, 1, 1])
        self.assertEqual(N.p, 1)
        N = SBF.SplineBaseFunction([0, 0, 0.2, 0.6, 1, 1])
        self.assertEqual(N.p, 1)
        N = SBF.SplineBaseFunction([0, 0, 0, 0.5, 1, 1, 1])
        self.assertEqual(N.p, 2)
        N = SBF.SplineBaseFunction([0, 0, 0, 0.2, 0.6, 1, 1, 1])
        self.assertEqual(N.p, 2)
        N = SBF.SplineBaseFunction([0, 0, 0, 0, 0.5, 1, 1, 1, 1])
        self.assertEqual(N.p, 3)
        N = SBF.SplineBaseFunction([0, 0, 0, 0, 0.2, 0.6, 1, 1, 1, 1])
        self.assertEqual(N.p, 3)

    def test_ValuesOfN(self):
        N = SBF.SplineBaseFunction([0, 0, 1, 1])
        self.assertEqual(N.n, 2)
        N = SBF.SplineBaseFunction([0, 0, 0, 1, 1, 1])
        self.assertEqual(N.n, 3)
        N = SBF.SplineBaseFunction([0, 0, 0, 0, 1, 1, 1, 1])
        self.assertEqual(N.n, 4)
        N = SBF.SplineBaseFunction([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
        self.assertEqual(N.n, 5)

        N = SBF.SplineBaseFunction([0, 0, 0.5, 1, 1])
        self.assertEqual(N.n, 3)
        N = SBF.SplineBaseFunction([0, 0, 0.2, 0.6, 1, 1])
        self.assertEqual(N.n, 4)
        N = SBF.SplineBaseFunction([0, 0, 0, 0.5, 1, 1, 1])
        self.assertEqual(N.n, 4)
        N = SBF.SplineBaseFunction([0, 0, 0, 0.2, 0.6, 1, 1, 1])
        self.assertEqual(N.n, 5)
        N = SBF.SplineBaseFunction([0, 0, 0, 0, 0.5, 1, 1, 1, 1])
        self.assertEqual(N.n, 5)
        N = SBF.SplineBaseFunction([0, 0, 0, 0, 0.2, 0.6, 1, 1, 1, 1])
        self.assertEqual(N.n, 6)

    def test_getEvaluationFunctions_p1n2(self):
        U = [0, 0, 1, 1]  # p = 1, n = 2
        N = SBF.SplineBaseFunction(U)

        N[0, 0]
        N[1, 0]
        N[2, 0]
        N[0, 1]
        N[1, 1]
        N[2, 1]
        N[:, 0]
        N[:, 1]
        N[:]

    def test_getEvaluationFunctions_p1n3(self):
        U = [0, 0, 0.5, 1, 1]  # p = 1, n = 3
        N = SBF.SplineBaseFunction(U)

        N[0, 0]
        N[1, 0]
        N[2, 0]
        N[3, 0]
        N[0, 1]
        N[1, 1]
        N[2, 1]
        N[3, 1]
        N[:, 0]
        N[:, 1]
        N[:]

    def test_findSpots(self):
        U = [0, 0, 0.2, 0.4, 0.5, 0.6, 0.8, 1, 1]   # p = 1, n =7
        N = SBF.SplineBaseFunction(U).evalfunction()
        self.assertEqual(N.spot(0), 1)
        self.assertEqual(N.spot(0.1), 1)
        self.assertEqual(N.spot(0.2), 2)
        self.assertEqual(N.spot(0.3), 2)
        self.assertEqual(N.spot(0.4), 3)
        self.assertEqual(N.spot(0.5), 4)
        self.assertEqual(N.spot(0.6), 5)
        self.assertEqual(N.spot(0.7), 5)
        self.assertEqual(N.spot(0.8), 6)
        self.assertEqual(N.spot(0.9), 6)
        self.assertEqual(N.spot(1.0), 7)
        array = np.linspace(0, 1, 11)  # (0, 0.1, 0.2, ..., 0.9, 1.0)
        suposedspots = N.spot(array)
        correctspots = [1, 1, 2, 2, 3, 4, 5, 5, 6, 6, 7]
        np.testing.assert_equal(suposedspots, correctspots)

    def test_somesinglevalues_p1n2(self):
        U = [0, 0, 1, 1]  # p = 1, n = 2
        N = SBF.SplineBaseFunction(U)
        self.assertEqual(N[0, 0](0.0), 0)
        self.assertEqual(N[0, 0](0.5), 0)
        self.assertEqual(N[0, 0](1.0), 0)
        self.assertEqual(N[1, 0](0.0), 1)
        self.assertEqual(N[1, 0](0.5), 1)
        self.assertEqual(N[1, 0](1.0), 1)
        self.assertEqual(N[0, 1](0.0), 1)
        self.assertEqual(N[0, 1](0.5), 0.5)
        self.assertEqual(N[0, 1](1.0), 0)
        self.assertEqual(N[1, 1](0.0), 0)
        self.assertEqual(N[1, 1](0.5), 0.5)
        self.assertEqual(N[1, 1](1.0), 1)

    def test_somesinglevalues_p2n3(self):
        U = [0, 0, 0, 1, 1, 1]  # p = 2, n = 3
        N = SBF.SplineBaseFunction(U)
        self.assertEqual(N[0, 0](0.0), 0)
        self.assertEqual(N[0, 0](0.5), 0)
        self.assertEqual(N[0, 0](1.0), 0)
        self.assertEqual(N[1, 0](0.0), 0)
        self.assertEqual(N[1, 0](0.5), 0)
        self.assertEqual(N[1, 0](1.0), 0)
        self.assertEqual(N[2, 0](0.0), 1)
        self.assertEqual(N[2, 0](0.5), 1)
        self.assertEqual(N[2, 0](1.0), 1)
        self.assertEqual(N[0, 1](0.0), 0)
        self.assertEqual(N[0, 1](0.5), 0)
        self.assertEqual(N[0, 1](1.0), 0)
        self.assertEqual(N[1, 1](0.0), 1)
        self.assertEqual(N[1, 1](0.5), 0.5)
        self.assertEqual(N[1, 1](1.0), 0)
        self.assertEqual(N[2, 1](0.0), 0)
        self.assertEqual(N[2, 1](0.5), 0.5)
        self.assertEqual(N[2, 1](1.0), 1)
        self.assertEqual(N[0, 2](0.0), 1)
        self.assertEqual(N[0, 2](0.5), 0.25)
        self.assertEqual(N[0, 2](1.0), 0)
        self.assertEqual(N[1, 2](0.0), 0)
        self.assertEqual(N[1, 2](0.5), 0.5)
        self.assertEqual(N[1, 2](1.0), 0)
        self.assertEqual(N[2, 2](0.0), 0)
        self.assertEqual(N[2, 2](0.5), 0.25)
        self.assertEqual(N[2, 2](1.0), 1)

    def test_tablevalues_p1n2(self):
        U = [0, 0, 1, 1]  # p = 1, n = 2
        utest = np.linspace(0, 1, 11)
        N = SBF.SplineBaseFunction(U)
        N0 = N[:, 0]
        N1 = N[:, 1]
        M0test = N0(utest)
        M0good = np.array([[0]*11,[1]*11])
        np.testing.assert_allclose(M0test, M0good)

        M1test = N1(utest)
        M1good = np.array([np.linspace(1, 0, 11), np.linspace(0, 1, 11)])
        np.testing.assert_allclose(M1test, M1good)

    def test_tablevalues_p1n3(self):
        U = [0, 0, 0.5, 1, 1]  # p = 1, n = 3
        utest = np.linspace(0, 1, 11)
        N = SBF.SplineBaseFunction(U)
        N0 = N[:, 0]
        N1 = N[:, 1]
        M0test = N0(utest)
        M0good = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
        np.testing.assert_allclose(M0test, M0good)

        M1test = N1(utest)
        M1good = [[1.0, 0.8, 0.6, 0.4, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0],
                  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]]
        np.testing.assert_allclose(M1test, M1good)


    def test_tablevalues_p2n3(self):
        U = [0, 0, 0, 1, 1, 1]  # p = 2, n = 3
        utest = np.linspace(0, 1, 11)
        N = SBF.SplineBaseFunction(U)
        N0 = N[:, 0]
        N1 = N[:, 1]
        N2 = N[:, 2]

        M0test = N0(utest)
        M0good = np.array([[0]*11,
                           [0]*11,
                           [1]*11])
        np.testing.assert_allclose(M0test, M0good)

        M1test = N1(utest)
        M1good = np.array([[0]*11,
                           np.linspace(1, 0, 11),
                           np.linspace(0, 1, 11)])
        np.testing.assert_allclose(M1test, M1good)

        M2test = N2(utest)
        M2good = np.array([[1.0, 0.81, 0.64, 0.49, 0.36, 0.25, 0.16, 0.09, 0.04, 0.01, 0.],
                           [0.,  0.18, 0.32, 0.42, 0.48, 0.50, 0.48, 0.42, 0.32, 0.18, 0.],
                           [0.,  0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.]])
        np.testing.assert_allclose(M2test, M2good)

    def test_tablevalues_p2n4(self):
        U = [0, 0, 0, 0.5, 1, 1, 1]  # p = 2, n = 4
        utest = np.linspace(0, 1, 11)
        N = SBF.SplineBaseFunction(U)
        N0 = N[:, 0]
        N1 = N[:, 1]
        N2 = N[:, 2]

        M0test = N0(utest)
        M0good = np.array([[0]*11,
                           [0]*11,
                           [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]])
        np.testing.assert_allclose(M0test, M0good)

        M1test = N1(utest)
        M1good = np.array([[0]*11,
                           [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0],
                           [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]])
        np.testing.assert_allclose(M1test, M1good)

        M2test = N2(utest)
        M2good = np.array([[ 1, 0.64, 0.36, 0.16, 0.04, 0.0, 0.00, 0.00, 0.00, 0.00, 0],
                           [ 0, 0.34, 0.56, 0.66, 0.64, 0.5, 0.32, 0.18, 0.08, 0.02, 0],
                           [ 0, 0.02, 0.08, 0.18, 0.32, 0.5, 0.64, 0.66, 0.56, 0.34, 0],
                           [ 0, 0.00, 0.00, 0.00, 0.00, 0.0, 0.04, 0.16, 0.36, 0.64, 1]])
        np.testing.assert_allclose(M2test, M2good)

    def test_tablevalues_p3n4(self):
        U = [0, 0, 0, 0, 1, 1, 1, 1]  # p = 3, n = 4
        utest = np.linspace(0, 1, 11)
        N = SBF.SplineBaseFunction(U)
        N0 = N[:, 0]
        N1 = N[:, 1]
        N2 = N[:, 2]
        N3 = N[:, 3]

        M0test = N0(utest)
        M0good = np.array([[0]*11,
                           [0]*11,
                           [0]*11,
                           [1]*11])
        np.testing.assert_allclose(M0test, M0good)

        M1test = N1(utest)
        M1good = np.array([[0]*11,
                           [0]*11,
                           np.linspace(1, 0, 11),
                           np.linspace(0, 1, 11)])
        np.testing.assert_allclose(M1test, M1good)

        M2test = N2(utest)
        M2good = np.array([[0]*11,
                           [1.0, 0.81, 0.64, 0.49, 0.36, 0.25, 0.16, 0.09, 0.04, 0.01, 0.],
                           [0.,  0.18, 0.32, 0.42, 0.48, 0.50, 0.48, 0.42, 0.32, 0.18, 0.],
                           [0.,  0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.]])
        np.testing.assert_allclose(M2test, M2good)

        M3test = N3(utest)
        M3good = np.array([[ 1, 0.729, 0.512, 0.343, 0.216, 0.125, 0.064, 0.027, 0.008, 0.001, 0],
                           [ 0, 0.243, 0.384, 0.441, 0.432, 0.375, 0.288, 0.189, 0.096, 0.027, 0],
                           [ 0, 0.027, 0.096, 0.189, 0.288, 0.375, 0.432, 0.441, 0.384, 0.243, 0],
                           [ 0, 0.001, 0.008, 0.027, 0.064, 0.125, 0.216, 0.343, 0.512, 0.729, 1]])
        diff = M3test - M3good
        np.testing.assert_allclose(M3test, M3good)

    def test_tablevalues_p3n5(self):
        U = [0, 0, 0, 0, 0.5, 1, 1, 1, 1]  # p = 3, n = 5
        utest = np.linspace(0, 1, 11)
        N = SBF.SplineBaseFunction(U)
        N0 = N[:, 0]
        N1 = N[:, 1]
        N2 = N[:, 2]
        N3 = N[:, 3]

        M0test = N0(utest)
        M0good = np.array([[0]*11,
                           [0]*11,
                           [0]*11,
                           [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]])
        np.testing.assert_allclose(M0test, M0good)

        M1test = N1(utest)
        M1good = np.array([[0]*11,
                           [0]*11,
                           [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0],
                           [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]])
        np.testing.assert_allclose(M1test, M1good)

        M2test = N2(utest)
        M2good = np.array([[0]*11,
                           [ 1, 0.64, 0.36, 0.16, 0.04, 0.0, 0.00, 0.00, 0.00, 0.00, 0],
                           [ 0, 0.34, 0.56, 0.66, 0.64, 0.5, 0.32, 0.18, 0.08, 0.02, 0],
                           [ 0, 0.02, 0.08, 0.18, 0.32, 0.5, 0.64, 0.66, 0.56, 0.34, 0],
                           [ 0, 0.00, 0.00, 0.00, 0.00, 0.0, 0.04, 0.16, 0.36, 0.64, 1]])
        np.testing.assert_allclose(M2test, M2good)

        M3test = N3(utest)
        M3good = np.array([[ 1, 0.512, 0.216, 0.064, 0.008, 0.000, 0.000, 0.000, 0.000, 0.000, 0],
                           [ 0, 0.434, 0.592, 0.558, 0.416, 0.250, 0.128, 0.054, 0.016, 0.002, 0],
                           [ 0, 0.052, 0.176, 0.324, 0.448, 0.500, 0.448, 0.324, 0.176, 0.052, 0],
                           [ 0, 0.002, 0.016, 0.054, 0.128, 0.250, 0.416, 0.558, 0.592, 0.434, 0],
                           [ 0, 0.000, 0.000, 0.000, 0.000, 0.000, 0.008, 0.064, 0.216, 0.512, 1]])
        np.testing.assert_allclose(M3test, M3good)

if __name__ == "__main__":
    unittest.main()
