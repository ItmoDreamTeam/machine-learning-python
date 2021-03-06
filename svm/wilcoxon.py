import svm.enumerator


def wilcoxon(a: [], b: []) -> {}:
    """
    Wilcoxon test \n
    Null hypothesis: difference between the pairs follows a symmetric distribution around zero. \n
    If the test statistic T <= critical_value, the null hypothesis is rejected. \n
    :return: True if null hypothesis is true, False otherwise, T, critical_value, p-value
    """
    differences = sorted([b[i] - a[i] for i in range(len(a))], key=abs)
    ranks = {i + 1: difference for i, difference in enumerate(differences)}
    T = min(sum(filter(lambda rank: ranks[rank] > 0, ranks)), sum(filter(lambda rank: ranks[rank] < 0, ranks)))
    W = sum(map(lambda rank: 1 if ranks[rank] > 0 else -1 if ranks[rank] < 0 else 0 * rank, ranks))
    cv = critical_value(len(a))
    return {
        "Null hypothesis": T > cv,
        "test statistic": T,
        "critical value": cv,
        "p-value": calculate_p_value(ranks, cv),
        "p-value as normal": calculate_p_value_as_normal(W, len(a))
    }


def critical_value(N: int) -> int:
    """
    α=0.05, two-tailed test \n
    Two-tailed: most common, when we want to see if A > B or A < B or A = B \n
    One-tailed: having a specific prediction (e.g., A is higher than B), we are completely uninterested
    in the possibility that the opposite outcome could be true \n
    :param N: number of data point, 6 &lt= N &lt= 20
    """
    return ([-1] * 6 + [1, 2, 4, 6, 8, 11, 14, 17, 21, 25, 30, 35, 40, 46, 52])[N]


def calculate_p_value_as_normal(W: int, n: int) -> float:
    μ = n * (n + 1) / 4
    σ = (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
    z = (W - μ) / σ
    return area_under_z(z) * 2


def area_under_z(z: float) -> float:
    e = 2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274274663919320030599218174135966290435729003342952605956307381323286279434907632338298807531952510190115738341879307021540891499348841675092447614606680
    pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091
    z = abs(z)
    Dz = 0.001
    result = 0
    while z < 10:
        result += e ** (-z ** 2 / 2) / (2 * pi) ** 0.5 * Dz
        z += Dz
    return result


def calculate_p_value(ranks: [int], T0: int) -> float:
    n = len(ranks)
    values = [svm.enumerator.Value(0, 1) for i in range(n)]
    enumerator = svm.enumerator.Enumerator(values)
    k = 0
    while True:
        current_ranks = {i + 1: 1 if values[i].value else -1 * ranks[i + 1] for i in range(n)}
        T = min(sum(filter(lambda rank: current_ranks[rank] > 0, current_ranks)),
                sum(filter(lambda rank: current_ranks[rank] < 0, current_ranks)))
        if T <= T0:
            k += 1
        if not enumerator.next():
            break
    return k / 2 ** n


knn_data = [
    0.757895,
    0.754098,
    0.796460,
    0.756757,
    0.813559,
    0.800000,
    0.803738,
    0.779661,
    0.784000,
    0.775862
]
svm_data = [
    0.857143,
    0.833333,
    0.785714,
    0.828829,
    0.831858,
    0.821429,
    0.831858,
    0.834783,
    0.810811,
    0.827586
]

if __name__ == '__main__':
    print(wilcoxon(knn_data, svm_data))
