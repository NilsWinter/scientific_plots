import matplotlib.pyplot as plt
import scientific_plots as sp
import seaborn as sns


iris = sns.load_dataset('iris')
x, y = iris['sepal_length'], iris['sepal_width']

plt.figure(figsize=(2, 2))
plt.scatter(x, y)
plt.ylabel('Sepal Width')
plt.xlabel('Sepal Length')
plt.tight_layout()
plt.savefig('../figures/scatter_default.pdf')
plt.show()

with plt.style.context(sp.get_style('mmll')):
    fig, ax = plt.subplots(figsize=(2, 2))
    plt.scatter(x, y)
    plt.ylabel('Sepal Width')
    plt.xlabel('Sepal Length')
    sp.polish(fig, ax)
    plt.savefig('../figures/scatter_mmll.pdf')
    plt.show()



