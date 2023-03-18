from collections import deque
class Color_Mapper:
    def __init__(self):
        self.frequency_bin_energies = []
        self.means_q = deque()
        self.MEANS_Q_LEN = 5
    def update_frequencies(self, frequency_bin_energies):
        if len(frequency_bin_energies) < 400:
            return False
        self.frequency_bin_energies = frequency_bin_energies[:100]


        return True

    def __update_means_q(self):
        if len(self.means_q) == self.MEANS_Q_LEN:
            self.means_q.popleft()
        self.means_q.append(self.__get_mean(self.frequency_bin_energies))
    def __get_mean(self,arr):
        return round((sum(arr)/len(arr)))
    def calculate_power(self):
        max_power = 80000
        # if len(self.means_q) == self.MEANS_Q_LEN:
        #     max_power = max(self.means_q)
        power = round((sum(self.frequency_bin_energies)/len(self.frequency_bin_energies))/max_power,2)
        if power > 1.0:
            return 1.0
        return power

    def get_average(self):
        return round((sum(self.frequency_bin_energies) / len(self.frequency_bin_energies)), 2)






