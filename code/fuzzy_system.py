import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class ClimateFuzzySystem:
    def __init__(self):
        # 1. Вхідні змінні (Температура та Вологість)
        self.temp = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
        self.hum = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')

        # 2. Вихідна змінна (Потужність клімат-системи 0-100%)
        self.power = ctrl.Consequent(np.arange(0, 101, 1), 'power')

        # Жорстко встановлюємо метод "Centroid"
        self.power.defuzzify_method = 'centroid'

        self._build_membership_functions()
        self._build_rules()

        self.system = ctrl.ControlSystem(self.rules)
        self.simulation = ctrl.ControlSystemSimulation(self.system)

    def _build_membership_functions(self):
        # Функції належності для Температури
        self.temp['cold'] = fuzz.trapmf(self.temp.universe, [0, 0, 15, 20])
        self.temp['normal'] = fuzz.trimf(self.temp.universe, [18, 22, 26])
        self.temp['hot'] = fuzz.trapmf(self.temp.universe, [24, 28, 40, 40])

        # Функції належності для Вологості
        self.hum['dry'] = fuzz.trapmf(self.hum.universe, [0, 0, 30, 45])
        self.hum['comfort'] = fuzz.trimf(self.hum.universe, [35, 50, 65])
        self.hum['wet'] = fuzz.trapmf(self.hum.universe, [55, 70, 100, 100])

        # Функції належності для Потужності (Низька, Середня, Висока)
        self.power['low'] = fuzz.trapmf(self.power.universe, [0, 0, 20, 40])
        self.power['medium'] = fuzz.trimf(self.power.universe, [30, 50, 70])
        self.power['high'] = fuzz.trapmf(self.power.universe, [60, 80, 100, 100])

    def _build_rules(self):
        # 9 продукційних правил
        self.rules = [
            ctrl.Rule(self.temp['cold'] & self.hum['dry'], self.power['low']),
            ctrl.Rule(self.temp['cold'] & self.hum['comfort'], self.power['low']),
            ctrl.Rule(self.temp['cold'] & self.hum['wet'], self.power['low']),

            ctrl.Rule(self.temp['normal'] & self.hum['dry'], self.power['low']),
            ctrl.Rule(self.temp['normal'] & self.hum['comfort'], self.power['medium']),
            ctrl.Rule(self.temp['normal'] & self.hum['wet'], self.power['medium']),

            ctrl.Rule(self.temp['hot'] & self.hum['dry'], self.power['medium']),
            ctrl.Rule(self.temp['hot'] & self.hum['comfort'], self.power['high']),
            ctrl.Rule(self.temp['hot'] & self.hum['wet'], self.power['high'])
        ]

    def compute(self, t, h):
        # Обчислення (завжди центроїд)
        self.simulation.input['temperature'] = t
        self.simulation.input['humidity'] = h
        self.simulation.compute()

        return self.simulation.output.get('power', 0)