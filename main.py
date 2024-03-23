from machine import PWM, Pin
from time import sleep_ms
from frequency_counter import calc_freq

if __name__ == "__main__":
    pulse_freq = 1_000
    pwm = PWM(Pin(23), freq=pulse_freq)
    pin = 22
    print("measured_frequency,expected_frequency,percentage_difference")
    for pulse_freq in range(10, 500_010, 1_000):
        pwm.freq(pulse_freq)
        sleep_ms(10)
        freq = calc_freq(pin)
        perc_diff = 100*abs((freq - pulse_freq)/pulse_freq)
        print(f"{freq:.2f},{pwm.freq()},{perc_diff:.2f}")
        sleep_ms(1)
