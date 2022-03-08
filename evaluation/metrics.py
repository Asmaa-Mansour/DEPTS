# adopt from https://github.com/ElementAI/N-BEATS
import os
"""
Metrics functions using numpy arrays.
"""
import numpy as np

Forecast = np.ndarray
Target = np.ndarray


def mase(forecast: Forecast, insample: np.ndarray, outsample: Target, frequency: int) -> np.ndarray:
    """
    MASE loss as defined in "Scaled Errors" https://robjhyndman.com/papers/mase.pdf

    :param forecast: Forecast values. Shape: batch, time_o
    :param insample: Insample values. Shape: batch, time_i
    :param outsample: Target values. Shape: batch, time_o
    :param frequency: Frequency value
    :return: Same shape array with error calculated for each time step
    """
    return np.mean(np.abs(forecast - outsample)) / np.mean(np.abs(insample[:-frequency] - insample[frequency:]))


def nd(forecast: Forecast, target: Target) -> float:
    """
    Normalized deviation as defined in https://www.cs.utexas.edu/~rofuyu/papers/tr-mf-nips.pdf

    :param forecast: Forecast values. Shape: batch, time
    :param target: Target values. Shape: batch, time
    :return: Error value
    """
    return np.mean(np.abs(target - forecast)) / np.mean(np.abs(target))


def nrmse(forecast: Forecast, target: Target) -> float:
    """
    Normalized RMSE as defined in https://www.cs.utexas.edu/~rofuyu/papers/tr-mf-nips.pdf

    :param forecast: Forecast values. Shape: batch, time
    :param target: Target values. Shape: batch, time
    :return: Error values
    """
    return np.sqrt(np.mean(np.power((forecast - target), 2))) / (np.mean(np.abs(target)))
     

def mape(forecast: Forecast, target: Target) -> np.ndarray:
    """
    MAPE loss as defined in: https://en.wikipedia.org/wiki/Mean_absolute_percentage_error

    :param forecast: Predicted values.
    :param target: Target values.
    :return: Same shape array with error calculated for each time step
    """
    return np.abs(forecast - target) / target


def smape_1(forecast: Forecast, target: Target) -> np.ndarray:
    """
    sMAPE loss as defined in "Appendix A" of
    http://www.forecastingprinciples.com/files/pdf/Makridakia-The%20M3%20Competition.pdf

    :param forecast: Forecast values. Shape: batch, time
    :param target: Target values. Shape: batch, time
    :return: Same shape array with error calculated for each time step
    """
    return 200 * np.abs(forecast - target) / (target + forecast)


def smape_2(forecast: Forecast, target: Target) -> np.ndarray:
    """
    sMAPE loss as defined in https://robjhyndman.com/hyndsight/smape/ (Makridakis 1993)

    :param forecast: Forecast values. Shape: batch, time
    :param target: Target values. Shape: batch, time
    :return: Same shape array with sMAPE calculated for each time step of each timeseries.
    """
    denom = np.abs(target) + np.abs(forecast)
    # divide by 1.0 instead of 0.0, in case when denom is zero the enumerator will be 0.0 anyway.
    denom[denom == 0.0] = 1.0
    return 200 * np.abs(forecast - target) / denom