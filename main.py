import os
from decmeasure import simulation, analysis

if __name__ == "__main__":
    simulation.main()
    datadirpath = os.path.join(os.getcwd(), "data")
    nameSeparators = [0, 1, 2, 3]
    analysis.main(nameSeparators, datadirpath)