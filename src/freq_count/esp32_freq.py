from machine import Pin, PCNT, PWM
from time import sleep_ms, sleep


class FrequencyMeter:
    def __init__(self, input_pin_number):
        self.input_pin = Pin(input_pin_number, Pin.IN)
        self.pcnt_unit = PCNT(0, self.input_pin)  # Using PCNT unit 0 and the input pin
        self.pcnt_unit.overflow(20000)  # Setting the overflow value
        self.pcnt_unit.filter(100)  # Apply a filter to ignore glitches; value to be adjusted
        self.sample_time = 1  # Sample time in seconds

    def read_frequency(self):
        self.pcnt_unit.clear()  # Clear the counter
        sleep(self.sample_time)  # Wait for the sample time
        pulse_count = self.pcnt_unit.value()  # Read the pulse count
        frequency = pulse_count / self.sample_time  # Calculate frequency
        return frequency


if __name__ == "__main__":
    pulse_freq = 1_000
    pwm = PWM(Pin(23), freq=pulse_freq)
    pin = 22
    fm = FrequencyMeter(pin)
    print("measured_frequency,expected_frequency,percentage_difference")
    for pulse_freq in range(10, 500_010, 1_000):
        pwm.freq(pulse_freq)
        sleep_ms(10)
        # freq = calc_freq(pin)
        freq = fm.read_frequency()
        perc_diff = 100 * abs((freq - pulse_freq) / pulse_freq)
        print(f"{freq:.2f},{pwm.freq()},{perc_diff:.2f}")
        sleep_ms(1)
