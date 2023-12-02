import numpy as np


class Model:

    def __init__(self, period, Z=lambda theta: 0, delay=1, epsilon=0.0001, abs_err=0.005, norm=1):
        self.period = period
        self.Z = Z

        self.epsilon = epsilon
        self.delay = delay

        self.norm = norm
        # simple wrapper around np.isclose
        # because of numerical error we can't use statements as a == b
        # we always have to consider some margin of error between two values
        self.near = lambda a, b: np.isclose(a, b, atol=abs_err)

        self.phase_speed = self.norm/self.period

        self.current_phase = 0
        self.current_time = 0

        self.pulse_times = list()

    def simulate(self, time):
        timeline = [self.current_time]
        phase = [self.current_phase]

        time += self.current_time
        while self.current_time <=  time:
          t, phases = self.__step()

          timeline.append(t)
          phase.append(phases[0])

          timeline.append(t + self.epsilon)
          phase.append(phases[1])

        return timeline, phase

    def __step(self):
        pulse_time = self.pulse_times[0] if self.pulse_times else np.Infinity

        delta_phase = self.norm - self.current_phase
        arriving_time_of_cycle = self.current_time + delta_phase / self.phase_speed

        if arriving_time_of_cycle < pulse_time:
            phase_before_event = self.norm
            phase_after_event = 0

            self.current_time = arriving_time_of_cycle

        else:
            delta_time = pulse_time - self.current_time
            phase_before_event = self.current_phase + delta_time * self.phase_speed
            phase_after_event = phase_before_event + self.Z(phase_before_event)

            self.pulse_times.pop(0)
            self.current_time = pulse_time

        if self.near(phase_after_event, self.norm) or self.near(phase_after_event, 0) or phase_after_event > self.norm:
            self.__send_pulse()

        self.current_phase = phase_after_event % self.norm

        return self.current_time, (phase_before_event, self.current_phase)

    def __send_pulse(self):
        self.pulse_times.append(self.current_time + self.delay)
