import math


def vector_add(v: list[float], w: list[float]) -> list[float]:
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def magnitude(v: list[float]) -> float:
    return math.sqrt(sum(v_i ** 2 for v_i in v))


def normalize(v: list[float]) -> list[float]:
    magnitude_v = magnitude(v)
    return [v_i / magnitude_v for v_i in v]


def scalar_product(v: list[float], k: float) -> list[float]:
    return [v_i * k for v_i in v]


def distance(v: list[float], w: list[float]) -> float:
    difference_vector = [v_i - w_i for v_i, w_i in zip(v, w)]
    return math.sqrt(sum(x_i ** 2 for x_i in difference_vector))
