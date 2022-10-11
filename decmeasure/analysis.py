import os
import pandas as pd
import matplotlib.pyplot as plt

def loadResultData(nameSeparators, datadirpath):
    data = []
    for i in range(len(nameSeparators)):
        fileName = "result" + str(nameSeparators[i]) + ".csv"
        filePath = os.path.join(datadirpath, fileName)
        data.append(pd.read_csv(filePath, sep="\t"))
    return data


def main(nameSeparators, datadirpath):
    try:
        result = loadResultData(nameSeparators, datadirpath)
    except:
        raise Exception("Fail to load data")
    xaxisResult = result[0].index
    resultColumns = result[0].columns
    plt.figure(constrained_layout=True)
    for cnt_columns in range(len(resultColumns)):
        legendString = []
        plt.subplot(2,2,cnt_columns+1)
        for i in range(len(nameSeparators)):
            plt.plot(xaxisResult, result[i][resultColumns[cnt_columns]])
            legendString.append("parameter" + str(i))
        plt.title(resultColumns[cnt_columns])
        plt.xlabel("Time (block)")
        plt.ylabel(resultColumns[cnt_columns])
        plt.legend(legendString)
    plt.show()

if __name__ == "__main__":
    maindirpath = os.path.join(os.getcwd(), os.pardir)
    datadirpath = os.path.join(maindirpath, "data")
    nameSeparators = [0, 1, 2, 3]
    main(nameSeparators, datadirpath)