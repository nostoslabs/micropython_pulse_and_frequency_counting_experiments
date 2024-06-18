from machine import time_pulse_us, disable_irq, enable_irq


def get_pulse_width_us_forum(pin: int) -> int:
    """
    Get the frequency of the input signal
    :param pin: input pin as int
    :return: frequency of the input signal
    """
    state = disable_irq()
    time_pulse_us(pin, 1, 1_000_000)
    pw = time_pulse_us(pin, 1, 1_000_000)
    enable_irq(state)
    state = disable_irq()
    time_pulse_us(pin, 0, 1_000_000)
    pw += time_pulse_us(pin, 0, 1_000_000)
    enable_irq(state)
    return pw


def get_pulse_period_us(pin: int) -> int:
    """
    Get the pulse period of the input signal
    :param pin: input pin as int
    :return: pulse period of the input signal
    """
    return time_pulse_us(pin, 1, 1_000_000) + time_pulse_us(pin, 0, 1_000_000)
    return pw


def calc_freq(pin: int, alpha=0.1, iterations=100) -> float:
    """
    Calculate the frequency of the input signal and filter with a Single Pole IIR filter
    :param pin: input pin as int
    :return: frequency of the input signal
    """
    y_n = 0
    beta = 1 - alpha

    for i in range(iterations):
        pw = get_pulse_period_us(pin)
        y_n = alpha * pw + beta * y_n
    return 1 / (y_n * 1e-6)
