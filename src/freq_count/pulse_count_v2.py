from machine import Pin, PWM, Timer
from time import sleep, sleep_ms
from uctypes import UINT32
from math import ceil

pulse_count_pin = Pin(22, Pin.IN, Pin.PULL_UP)
pulse_freqs = range(32000, 200000, 5000)

# Preallocate array we're going to stop values in.
pulse_stats = [(0, 0)] * len(pulse_freqs)

pulses: float = 0.001
tim0 = Timer(0)


def timer_done(k):
    global pulse_count_pin
    pulse_count_pin.irq(handler=None)


def ISR(boo):
    global pulses
    pulses += 1


for cnt, pulse_freq in enumerate(pulse_freqs):
    pwm = PWM(Pin(23), freq=pulse_freq)
    sleep_ms(100)  # Stabilize PWM
    pulses = 0
    if pulse_freq > 30000:
        timer_ms = 1
        pulse_count_pin.irq(trigger=Pin.IRQ_RISING, handler=ISR)
        tim0.init(period=timer_ms, mode=Timer.ONE_SHOT, callback=timer_done)
        sleep_ms(timer_ms)
        pulse_stats[cnt] = (pulse_freq, 1000 * pulses)
        print(f"PWM -vs- Calc: {pwm.freq()},{1000 * pulses}")
    else:
        timer_ms = 1000
        pulse_count_pin.irq(trigger=Pin.IRQ_RISING, handler=ISR)
        tim0.init(period=timer_ms, mode=Timer.ONE_SHOT, callback=timer_done)
        sleep_ms(timer_ms)
        pulse_stats[cnt] = (pulse_freq, pulses)
        print(f"PWM -vs- Calc: {pwm.freq()},{pulses}")

print("Percent Difference,Timer,Frequency,Pulses,Calculated Frequency")
for freq, my_pulses in pulse_stats:
    perc_diff: float = 100.0 * (freq - my_pulses) / freq
    calc_freq: float = my_pulses
    print(f"{perc_diff:0.1f},{timer_ms},{freq},{my_pulses},{calc_freq:0.3f}")
