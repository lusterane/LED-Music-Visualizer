from collections import deque
from statistics import mean
class Color_Mapper:
    def __init__(self):
        self.frequency_bin_energies = []
        self.frequencies_for_power = []

        self.power_mean_q = []
        self.POWER_MEAN_Q_LEN = 5
        self.MAX_POWER = 150000
    def update_frequencies(self, frequency_bin_energies):
        if len(frequency_bin_energies) < 400:
            return False
        self.frequency_bin_energies = frequency_bin_energies
        self.frequencies_for_power = frequency_bin_energies[:150]

        # processing
        self.__update_power_mean_q()
        # self.__update_max_power()
        return True
    def __update_power_mean_q(self):
        if len(self.power_mean_q) == self.POWER_MEAN_Q_LEN:
            self.power_mean_q.pop(0)
        self.power_mean_q.append(self.__calculate_current_power())

    def __update_max_power(self):
        self.MAX_POWER = max(self.frequencies_for_power)//5
    def __calculate_current_power(self):
        # if len(self.means_q) == self.MEANS_Q_LEN:
        #     max_power = max(self.means_q)
        power = round(mean(self.frequencies_for_power)/self.MAX_POWER,2)
        if power > 1.0:
            return 1.0
        return power
    def get_power(self):
        return self.__calculate_current_power()






