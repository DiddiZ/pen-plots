import numpy as np


def is_colinear(points):
    return np.linalg.matrix_rank(points - points[0]) < 2


def fourier_min_error(points, threshold, max_k=None):
    """
    Computes Fourier transformation of the lowest required order s.t. the mean squared approximation error is below
    `threshold`.

    This can be much faster than using FFT, especially if there are many points and the approixmation only requires a
    low order.
    """
    N = len(points)
    y = points[:, 0] + 1j * points[:, 1]

    t = np.linspace(0, 1, N, endpoint=False)

    k = 0
    freq = [0]
    c = [np.mean(y)]
    approx = np.tile(c[0], N)

    while max_k is None or k < max_k:
        k += 1

        # Compute next order transformation
        freq.extend((-k, k))
        c.extend((
            np.mean(y * np.exp(k * 2j * np.pi * t)),
            np.mean(y * np.exp(-k * 2j * np.pi * t)),
        ))

        # Update running approximation
        approx += c[-2] * np.exp(freq[-2] * 2j * np.pi * t) + c[-1] * np.exp(freq[-1] * 2j * np.pi * t)

        mse = np.mean(np.square(np.abs(approx - y)))  # Calculate error
        if mse <= threshold:
            break

    return np.array(freq), np.array(c)


def fourier_fft(points):
    """
    Applies fast fourier transformation to a list of two-dimensional points.
    """
    N = len(points)
    y = points[:, 0] + 1j * points[:, 1]  # Convert to complex

    freq = np.fft.fftfreq(N, 1 / N)
    c = np.fft.fft(y) / N

    return freq, c


def fourier_fft_fixed_order(points, k):
    """
    Computes Fourier transformation of order `k` by selectiong corresponding component using Fast Fourier
    Transformation. Therefore the maximum order is bound by `(N - 1) // 2`.
    """
    N = len(points)
    if k > (N - 1) // 2:
        raise ValueError("Order k can't be greater than %d" % ((N - 1) // 2))

    freq, c = fourier_fft(points)

    idx = np.concatenate([np.arange(k + 1), np.arange(N - k, N)])
    return freq[idx], c[idx]


def fourier_fft_min_error(points, threshold):
    """
    Computes Fourier transformation of the lowest required order s.t. the mean squared approximation error is below
    `threshold`.

    Selects components produces by Fast Fourier Transformation, therefore the maximum order is bound by `(N - 1) // 2`.
    """
    N = len(points)
    y = points[:, 0] + 1j * points[:, 1]
    freq = np.fft.fftfreq(N, 1 / N)
    c = np.fft.fft(y) / N
    t = np.linspace(0, 1, N, endpoint=False)

    approx = np.tile(c[0], N)
    for k in range(1, (N + 1) // 2):
        approx += c[k] * np.exp(freq[k] * 2j * np.pi * t) + c[-k] * np.exp(freq[-k] * 2j * np.pi * t)

        error = np.mean(np.square(np.abs(approx - y)))
        if error <= threshold:
            break

    idx = np.concatenate([np.arange(k + 1), np.arange(N - k, N)])
    return freq[idx], c[idx]


def sample_fourier(freq, c, n_samples):
    """
    Generates samples from a fourier transformed.
    """
    samples = np.empty((n_samples, 2))
    for i, t in enumerate(np.linspace(0, 1, n_samples)):
        s = np.sum(c * np.exp(freq * 2j * np.pi * t))
        samples[i] = np.real(s), np.imag(s)
    return samples
