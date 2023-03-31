from collections import deque
from statistics import mean
class Color_Mapper:
    def __init__(self):
        self.frequency_bin_energies = []
        self.frequencies_for_power = []

        self.MEAN_Q_LEN = 30
        self.MAX_FREQ_POWER = 200000
        self.color_freq_sections = 4

        self.power_mean_q = []
        self.color_mean_q = []
    def update_frequencies(self, frequency_bin_energies):
        if len(frequency_bin_energies) < 400:
            return False
        self.frequencies_for_color = frequency_bin_energies
        self.frequencies_for_power = frequency_bin_energies[:150] # bass level
        # self.__update_MAX_FREQ_POWER()

        # processing
        self.__update_power_mean_q()
        self.__update_color_mean_q()
        return True

    def __update_color_mean_q(self):
        if len(self.color_mean_q) == self.MEAN_Q_LEN:
            self.color_mean_q.pop(0)
        freq_sections = [0,0,0,0]
        k = len(self.frequencies_for_color)//self.color_freq_sections
        freq_sections[0] = self.__calculate_current_power(self.frequencies_for_color[:k])
        freq_sections[1] = self.__calculate_current_power(self.frequencies_for_color[k:2*k])
        freq_sections[2] = self.__calculate_current_power(self.frequencies_for_color[2*k:3*k])
        freq_sections[3] = self.__calculate_current_power(self.frequencies_for_color[3*k:])
        self.color_mean_q.append(freq_sections)
    def __update_power_mean_q(self):
        if len(self.power_mean_q) == self.MEAN_Q_LEN:
            self.power_mean_q.pop(0)
        self.power_mean_q.append(self.__calculate_current_power(self.frequencies_for_power))

    def __get_greatest_color_change(self):
        greatest_change_idx = self.color_freq_sections - 1
        if not self.color_mean_q:
            return greatest_change_idx
        section_diffs = [0,0,0,0]
        for i in range(self.color_freq_sections):
            section_diffs[i] = self.color_mean_q[-1][i] - self.color_mean_q[0][i]
        greatest_change_val = 0
        for i,diff in enumerate(section_diffs):
            if diff > greatest_change_val:
                greatest_change_idx = i
                greatest_change_val = diff

        return greatest_change_idx

    def __update_MAX_FREQ_POWER(self):
        self.MAX_FREQ_POWER = max(self.frequencies_for_power)//5
    def __calculate_current_power(self,freq):
        # if len(self.means_q) == self.MEANS_Q_LEN:
        #     MAX_FREQ_POWER = max(self.means_q)
        power = round(mean(freq)/self.MAX_FREQ_POWER,2)
        if power > 1.0:
            return 1.0
        return power
    def get_power(self):
        return self.__calculate_current_power(self.frequencies_for_power)

    def get_color(self):
        dominant_section = self.__get_greatest_color_change()
        if dominant_section == 0:
            # pink
            return [255,20,120]
        elif dominant_section == 1:
            # blue
            return [50, 83, 200]
        elif dominant_section == 2:
            # light blue
            return [250,50,83]
        else:
            # purple
            return [150,50,250]

        # if dominant_section == 0 or dominant_section == 1:
        #     return [250,0,0]
        # else:
        #     return [0,0,0]






