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
