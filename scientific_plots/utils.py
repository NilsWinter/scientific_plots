import os
import matplotlib.pyplot as plt
import seaborn as sns


def savefig(fname, dpi: int = 300, transparent: bool = False, **kwargs):
    extensions = ['.pdf', '.png', '.eps', '.svg', '.jpg']

    path, filename = os.path.split(fname)
    if filename:
        filename, ext = os.path.splitext(filename)
        if ext not in extensions:
            extensions.append(ext)
        path = os.path.join(path, filename)
    else:
        filename = os.path.basename(path)

    os.makedirs(path, exist_ok=True)

    for ext in extensions:
        plt.savefig(fname=os.path.join(path, filename+ext), dpi=dpi,
                    transparent=transparent, **kwargs)
    return


if __name__ == "__main__":
    iris = sns.load_dataset('iris')
    x, y = iris['sepal_length'], iris['sepal_width']

    plt.figure(figsize=(2, 2))
    plt.scatter(x, y)
    savefig('../figures/savefig_example/')
    savefig('../figures/savefig_example')
    savefig('../figures/savefig_example.png')
