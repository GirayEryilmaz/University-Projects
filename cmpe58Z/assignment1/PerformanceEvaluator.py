
import math
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import numpy as np


def get_data(data_num):
    with open("./data{}/data{}_Class_Labels.txt".format(data_num, data_num), 'r') as data_Class_Labels:
        labels = data_Class_Labels.read().split('\n')
        del labels[-1]

    similarity_matrix = pd.read_csv("./data{}/data{}_SM.txt".format(data_num, data_num), header=None)
    return labels, similarity_matrix.values


class PerformanceEvaluator:

    def __init__(self, similarity_matrix, labels, data_name="SM"):
        tril = np.tril_indices(len(similarity_matrix))
        similarity_matrix[tril] = math.nan
        self.SM = similarity_matrix
        self.labels = labels
        self.data_name = data_name

    def plot_ROC(self):
        """
        Plots ROC curve
        :return: None
        """
        lst = []
        for label_left, row in zip(self.labels, self.SM):
            for label_up, element in zip(self.labels, row):
                if label_left == label_up:  # genuine ones
                    lst.append(('gen', element))
                else:  # impostors
                    lst.append(('imp', element))
        s_prime = list(sorted(filter(lambda x: not math.isnan(x[1]), lst), key=lambda y: y[1]))

        gens_before = [0]
        for i, (category, sim_score) in enumerate(s_prime[:-1]):
            if category == 'gen':
                gens_before.append(gens_before[i] + 1)
            else:
                gens_before.append(gens_before[i])

        imps_after = [0]
        for i, (category, sim_score) in enumerate(reversed(s_prime[1:])):
            if category == 'imp':
                imps_after.append(imps_after[i] + 1)
            else:
                imps_after.append(imps_after[i])
        imps_after = list(reversed(imps_after))

        num_gen = sum(1 for x, _ in s_prime if x == 'gen')
        num_imp = sum(1 for x, _ in s_prime if x == 'imp')
        GMRs = list(map(lambda x: 1 - x / num_gen, gens_before))
        FARs = list(map(lambda x: x / num_imp, imps_after))
        plt.margins(x=0, y=0)
        plt.xlabel('FAR')
        plt.ylabel('GAR')
        plt.grid(b=True, linestyle='dashed')
        plt.xticks([x/10 for x in range(11)])
        plt.yticks([x/10 for x in range(11)])
        plt.plot(FARs, GMRs)
        plt.show()

    def plot_score_distribution(self):
        """
        Plots Genuine and Impostor Score Distribution
        :return: None
        """
        genuine_ones, impostors = self.__genuine_ones_and_impostors()
        go = pd.Series(genuine_ones, name='genuine')
        imps = pd.Series(impostors, name='imps')
        df = pd.concat([go, imps], axis=1)
        fig, ax = plt.subplots()
        df.plot(ax=ax, kind='kde', legend=False, title='Genuine and Impostor Score Distribution Plot')
        ax.set_xlabel('Score')
        ax.grid(axis='y')
        ax.set_facecolor('#d8dcd6')
        plt.show()

    def FRR_at_FAR(self, FAR):
        """

        :param FAR: false accept rate
        :return: false reject rate at given false accept rate
        """
        s = list(sorted(filter(lambda x: not math.isnan(x), self.SM.flatten())))

        def cost_for_FAR_search(t):
            FMR, FNMR = self.get_FMR_FNMR(t)
            return -FMR

        ip = self.__insertion_point_with_key(s, -FAR, 0, len(s), lambda x: cost_for_FAR_search(x))
        _, fnmr = self.get_FMR_FNMR(s[ip])
        return fnmr, s[ip]

    def find_err(self):
        """

        :return: equal error rate, err threshold similarity value
        """
        def err_cost(t):
            fmr, fnmr = self.get_FMR_FNMR(t)
            return fnmr - fmr

        s = list(sorted(filter(lambda x: not math.isnan(x), self.SM.flatten())))
        ip = PerformanceEvaluator.__insertion_point_with_key(s, 0, 0, len(s), err_cost)
        fmr, _ = self.get_FMR_FNMR(s[ip])
        return round(fmr, 7), (s[ip] + s[ip+1])/2

    def __genuine_ones_and_impostors(self):
        genuine_ones = []
        impostors = []
        for label_left, row in zip(self.labels, self.SM):
            for label_up, element in zip(self.labels, row):
                if math.isnan(element):
                    continue
                if label_left == label_up:
                    genuine_ones.append(element)
                else:
                    impostors.append(element)
        return genuine_ones, impostors

    def get_FMR_FNMR(self, threshold):
        counter = self.__evaluate(threshold)
        # TODO think of nan's at the diagonal
        FMR = counter['fp'] / (counter['fp'] + counter['tn'])
        FNMR = counter['fn'] / (counter['tp'] + counter['fn'])
        return FMR, FNMR

    def __evaluate(self, threshold):
        counter = Counter()
        for label_left, row in zip(self.labels, self.SM):
            for label_up, similarity_score in zip(self.labels, row):
                if math.isnan(similarity_score):
                    continue
                if label_left == label_up:  # genuine ones
                    if similarity_score >= threshold:
                        counter['tp'] += 1
                    else:
                        counter['fn'] += 1
                else:  # impostors
                    if similarity_score >= threshold:
                        counter['fp'] += 1
                    else:
                        counter['tn'] += 1
        return counter

    @staticmethod
    def __insertion_point_with_key(array, elem, low, high, key_func):  # high is not inclusive
        """
        In short, bisect with key function.
        A modified binary search algorithm. It uses a key function while searching.
        The elements of given array need not be sorted. But the results of key function applied to elements shall be so
        :param array: array to search
        :param elem: the value to search for
        :param low: lowest index of given array to start searching, inclusive
        :param high: 'highest index + 1' to search in the array, thus this value is not inclusive. ex., high=len(array)
        :param key_func: the function to be applied to element of array while searching
        :return:
        """
        mid = (low + high) // 2
        #     print(low,mid,high)
        if high == 0:
            return -1
        if mid == high:
            return high - 1

        score = key_func(array[mid])
        # print(score, low, mid, high)
        if elem == score:
            return mid
        elif elem > score:
            return PerformanceEvaluator.__insertion_point_with_key(array, elem, mid + 1, high, key_func)
        elif elem < score:
            return PerformanceEvaluator.__insertion_point_with_key(array, elem, low, mid, key_func)
