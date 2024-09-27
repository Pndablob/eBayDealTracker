import matplotlib.pyplot as plt


def plot(x, y):
    plt.style.use('seaborn-whitegrid')

    fig = plt.figure()
    ax = plt.axes()

    plt.scatter(x, y)
    plt.plot(x, y)

    plt.show()
