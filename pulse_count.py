from machine import Pin, Timer
from time import sleep, sleep_ms, time_ns


class PulseCounter:

    def __init__(self, input_pin_number: int, measurement_period_ms: int = 1000):
        self.measurement_period_ms = measurement_period_ms
        self.input_pin = Pin(input_pin_number, Pin.IN, Pin.PULL_UP)
        self.ticks = 0
        self.ticks_prev = 0
        self.pulse_width = 0

    def irq_handler(self, pin):
        self.ticks = time_ns()
        self.pulse_width = self.ticks - self.ticks_prev
        self.ticks_prev = self.ticks

    def measure(self):
        # Set up the interrupt
        self.input_pin.irq(trigger=Pin.IRQ_RISING, handler=self.irq_handler)
        sleep_ms(self.measurement_period_ms)
        self.input_pin.irq(handler=None)
        return self.pulse_width


if __name__ == "__main__":
    from machine import PWM
    fm = PulseCounter(22, 10)
    pulse_freqs = range(10, 50000, 3000)
    pulse_stats = [(1.0,1.0)] * len(pulse_freqs)
    
    for cnt, pulse_freq in enumerate(pulse_freqs):
        pwm = PWM(Pin(23), freq=pulse_freq)
        sleep_ms(100) # Stabilize PWM
        pulses = fm.measure()
        print(f"PWM -vs- Calc: {pwm.freq()},{pulses/1e9}")
        if pulses == 0: 
            pulse_stats[cnt] = (1, 1)
            continue
        else:
            pulse_stats[cnt] = (pulse_freq, 1e9/pulses)

    print("Percent Difference,Timer,Frequency,Pulses,Calculated Frequency")
    for freq, my_pulses in pulse_stats:
        perc_diff: float = 100.0 * (freq - my_pulses)/freq
        print(f"{perc_diff:0.1f},{freq},{my_pulses}")
