def wilcoxon(a: [], b: []) -> {}:
    """
    Wilcoxon test \n
    Null hypothesis: difference between the pairs follows a symmetric distribution around zero. \n
    If the test statistic T <= critical_value, the null hypothesis is rejected. \n
    :return: True if null hypothesis is true, False otherwise, T, critical_value
    """
    differences = sorted([b[i] - a[i] for i in range(len(a))], key=abs)
    ranks = {i + 1: difference for i, difference in enumerate(differences)}
    T = min(sum(filter(lambda rank: ranks[rank] > 0, ranks)), sum(filter(lambda rank: ranks[rank] < 0, ranks)))
    cv = critical_value(len(a))
    return {"Null hypothesis": T > cv, "test statistic": T, "critical value": cv}


def critical_value(N: int) -> int:
    """
    α=0.05, two-tailed test \n
    Two-tailed: most common, when we want to see if A > B or A < B or A = B \n
    One-tailed: having a specific prediction (e.g., A is higher than B), we are completely uninterested
    in the possibility that the opposite outcome could be true \n
    :param N: number of data point, 6 &lt= N &lt= 20
    :return:
    """
    return ([-1] * 6 + [1, 2, 4, 6, 8, 11, 14, 17, 21, 25, 30, 35, 40, 46, 52])[N]


knn = [
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
svm = [
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
    import scipy.stats

    print(wilcoxon(knn, svm))
    print(scipy.stats.wilcoxon(knn, svm))
