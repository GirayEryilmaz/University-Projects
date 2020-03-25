import sys
import pandas as pd
from PerformanceEvaluator import PerformanceEvaluator

sim_matrix_path = sys.argv[1]
labels_path = sys.argv[2]

with open(labels_path, 'r') as data_Class_Labels:
    labels = data_Class_Labels.read().split('\n')
    del labels[-1]

SM = pd.read_csv(sim_matrix_path, header=None).to_numpy()

pe = PerformanceEvaluator(SM, labels, sim_matrix_path)

err, sim_thld = pe.find_err()

print('ERR\t=\t{:.2%}'.format(err), '\t\t\t\twith threshold = {:.4f}'.format(sim_thld))

print("FRR\t=\t{:.2%}\t\t\tat FAR point 0.1%\t\twhere t = {:.3f}".format(*pe.FRR_at_FAR(FAR=0.001)))
print("FRR\t=\t{:.2%}\t\t\tat FAR point 1%\t\twhere t = {:.3f}".format(*pe.FRR_at_FAR(FAR=0.01)))
print("FRR\t=\t{:.2%}\t\t\tat FAR point 10%\t\twhere t = {:.3f}".format(*pe.FRR_at_FAR(FAR=0.1)))

pe.plot_score_distribution()

pe.plot_ROC()
