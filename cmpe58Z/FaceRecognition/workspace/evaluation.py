from sklearn.metrics import roc_curve, auc
import pandas as pd
from matplotlib import pyplot as plt

def plot_score_distribution(genuine_ones, impostors):
    """
    Plots Genuine and Impostor Score Distribution
    :return: None
    """
    go = pd.Series(genuine_ones, name='genuine')
    imps = pd.Series(impostors, name='imps')
    df = pd.concat([go, imps], axis=1)
    fig, ax = plt.subplots()
    df.plot(ax=ax, kind='kde', legend=False, title='Genuine and Impostor Score Distribution Plot')
    ax.set_xlabel('Score')
    ax.grid(axis='y')
    ax.set_facecolor('#d8dcd6')
    plt.show()

def plot_roc_curve(labels, similarities):
    fpr, tpr, thresholds = roc_curve(labels, similarities, pos_label=1)
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.5f)' % auc(fpr,tpr))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()
    return fpr, tpr, thresholds