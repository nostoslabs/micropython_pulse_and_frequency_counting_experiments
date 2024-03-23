import machine
import time

# Constants
CPU_FREQ = machine.freq()  # Get CPU frequency in Hz
R1 = 81982
R2 = 11955055
R_freq_high = R1
R_freq_low = R2 + R1
R_RATIO = R_freq_low / R_freq_high
pin_int = machine.Pin(16, machine.Pin.IN)  # D1
pin_trig = machine.Pin(3, machine.Pin.OUT)  # D3

# Volatile variables
ratio = 0.0
trig = 0
start = 0
period = 0
temp = 0

# Interrupt Service Routine
def isr(pin):
    global trig, start, period
    trig = time.ticks_cpu()
    period = machine.ticks_diff(trig, start)
    start = trig

# Setup
pin_int.irq(trigger=machine.Pin.IRQ_RISING, handler=isr)

# Main loop
while True:
    if trig != 0:
        pin_trig.value(1)
        time.sleep_ms(2000)
        period_high = period
        period_high_us = period_high / (CPU_FREQ / 1000000)  # Convert to microseconds
        print("Period Low: ", period_high_us, "us")
        print("Freq High: ", 1e6 / period_high_us, "kHz")
        print("")
        time.sleep_ms(10000)

        pin_trig.value(0)
        time.sleep_ms(2000)
        period_low = period
        period_low_us = period_low / (CPU_FREQ / 1000000)  # Convert to microseconds
        print("Period High: ", period_low_us, "us")
        print("Freq Low: ", 1e9 / period_low_us, "Hz")
        print("")

        ratio = 1 / (R_RATIO * (period_high / period_low))
        print("Ratio: ", ratio)
        time.sleep_ms(10000)

        time.sleep_ms(11000)
