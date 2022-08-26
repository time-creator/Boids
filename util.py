import math


Vector = list[float]


def vector_add(v: Vector, w: Vector) -> Vector:
    """Adds Vector v and Vector w."""
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def vector_sub(v: Vector, w: Vector) -> Vector:
    """Subtracts Vector w from Vector v."""
    return [v_i - w_i for v_i, w_i in zip(v, w)]


def scalar_product(v: Vector, k: float) -> Vector:
    return [v_i * k for v_i in v]


def scalar_division(v: Vector, k: float) -> Vector:
    """Divides the elements of the vector v by the scalar k."""
    return [v_i / k for v_i in v]


def magnitude(v: Vector) -> float:
    return math.sqrt(sum(v_i ** 2 for v_i in v))


def normalize(v: Vector) -> Vector:
    """Normalizes the Vector to have a magnitude of 1."""
    magnitude_v = magnitude(v)
    return [v_i / magnitude_v for v_i in v]


def distance(v: Vector, w: Vector) -> float:
    difference_vector = [v_i - w_i for v_i, w_i in zip(v, w)]
    return math.sqrt(sum(x_i ** 2 for x_i in difference_vector))


if __name__ == '__main__':
    # Test vector_add
    assert vector_add([4, 3, 2, 1], [6, 7, 8, 9]) == [10, 10, 10, 10]
    assert vector_add([-1, 1, -1, 1], [0, 0, 0, 0]) == [-1, 1, -1, 1]
    assert vector_add([35, 8, 123, 0], [1, 74, 78, 22]) == [36, 82, 201, 22]

    # Test vector_sub
    assert vector_sub([10, 10, 10, 10], [6, 7, 8, 9]) == [4, 3, 2, 1]
    assert vector_sub([-1, 1, -1, 1], [0, 0, 0, 0]) == [-1, 1, -1, 1]
    assert vector_sub([36, 82, 201, 22], [1, 74, 78, 22]) == [35, 8, 123, 0]

    # Test scalar_product

    # Test scalar_division
