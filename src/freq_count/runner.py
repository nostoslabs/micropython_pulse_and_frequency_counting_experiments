from time import sleep_ms
from machine import PWM, Pin
from pulse_width_measure import PulseWidthMeasure

if __name__ == "__main__":

    fm = PulseWidthMeasure(22, 10)
    pulse_freqs = range(10, 60000, 3000)
    pulse_stats = [(1.0, 1.0)] * len(pulse_freqs)

    for cnt, pulse_freq in enumerate(pulse_freqs):
        pwm = PWM(Pin(23), freq=pulse_freq)
        sleep_ms(100)  # Stabilize PWM
        pulses = fm.measure()
        print(f"PWM -vs- Calc: {pwm.freq()},{pulses / 1e9}")
        if pulses == 0:
            pulse_stats[cnt] = (1, 1)
            continue
        else:
            pulse_stats[cnt] = (pulse_freq, 1e9 / pulses)

    print("Percent Difference,Timer,Frequency,Pulses,Calculated Frequency")
    for freq, my_pulses in pulse_stats:
        perc_diff: float = 100.0 * (freq - my_pulses) / freq
        print(f"{perc_diff:0.1f},{freq},{my_pulses}")
