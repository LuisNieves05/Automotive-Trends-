# These small functions are used by more than one question.
from pathlib import Path
import hashlib
import platform
import numpy as np
import pandas as pd
import matplotlib

# Save graphs as image files, even when no plot window is available.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Find the data and results folder next to these Python files.
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
MPG = 'Real-World MPG'
HP = 'Horsepower (HP)'
ACC = 'Acceleration (0-60 time in seconds)'
PROD = 'Production (000)'


def load_data():
    # A dash or blank cell means missing data, not zero.
    data = pd.read_csv(ROOT / 'table_export.csv', na_values=['-', ''])
    data[MPG] = pd.to_numeric(data[MPG], errors='coerce')
    data[HP] = pd.to_numeric(data[HP], errors='coerce')
    data[ACC] = pd.to_numeric(data[ACC], errors='coerce')
    data[PROD] = pd.to_numeric(data[PROD], errors='coerce')
    # 'Prelim. 2025' becomes missing so it is left out of the year filters.
    data['year'] = pd.to_numeric(data['Model Year'], errors='coerce')
    return data


def fit(x, y, weights=None):
    # Convert the data columns to arrays of numbers.
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # Ordinary regression gives every point a weight of 1.
    # For weighted regression, the caller supplies production counts.
    if weights is None:
        w = np.ones(len(y))
    else:
        w = np.asarray(weights, dtype=float)

    if len(y) < 3:
        raise ValueError('At least three points are needed for this analysis.')
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError('The x and y values must be finite numbers.')
    if not np.all(np.isfinite(w)) or np.any(w <= 0):
        raise ValueError('All weights must be finite and greater than zero.')

    # The model is y = intercept + slope*x.
    # Each row of the equation matrix is [1, x]. The first column fits
    # the intercept, and the second column fits the slope.
    equation_matrix = np.column_stack([np.ones(len(x)), x])

    # Multiplying each equation by sqrt(weight) gives weighted least squares.
    # For ordinary regression sqrt(1) = 1, so the equations stay the same.
    square_root_weights = np.sqrt(w)
    weighted_matrix = equation_matrix * square_root_weights[:, None]
    weighted_y = y * square_root_weights
    coefficients = np.linalg.lstsq(weighted_matrix, weighted_y, rcond=None)[0]
    intercept = coefficients[0]
    slope = coefficients[1]

    predicted = intercept + slope * x
    residual = y - predicted

    # R² compares the model's squared errors with variation about the mean.
    squared_error = np.sum(w * residual**2)
    mean_y = np.average(y, weights=w)
    total_variation = np.sum(w * (y - mean_y)**2)
    if total_variation == 0:
        r_squared = float('nan')
    else:
        r_squared = 1 - squared_error / total_variation

    # RMSE has the same units as y (MPG or seconds).
    rmse = np.sqrt(squared_error / np.sum(w))

    # Use names so the question scripts can access each result clearly.
    results = {}
    results['intercept'] = float(intercept)
    results['slope'] = float(slope)
    results['r2'] = float(r_squared)
    results['rmse'] = float(rmse)
    results['predicted'] = predicted
    results['residual'] = residual
    return results


def report_fit(label, model, n, units):
    # Keep the same number of decimal places in every regression report.
    text = f'{label}: n = {n}\n'
    text += f'  intercept = {model["intercept"]:.6f}; slope = {model["slope"]:.8f} {units}\n'
    text += f'  R² = {model["r2"]:.6f}; RMSE = {model["rmse"]:.6f}\n'
    return text


def save_report(name, text):
    # Show the results in the terminal and save the same text for the README.
    OUT.mkdir(exist_ok=True)
    print(text)
    output_file = OUT / f'{name}_output.txt'
    output_file.write_text(text + '\n', encoding='utf-8')


def save_plot(fig, name):
    OUT.mkdir(exist_ok=True)
    output_file = OUT / f'{name}.png'
    fig.savefig(output_file, dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_environment():
    # Record package versions and a file fingerprint for reproducibility.
    text = f'Python {platform.python_version()}\n'
    text += f'NumPy {np.__version__}\n'
    text += f'pandas {pd.__version__}\n'
    text += f'Matplotlib {matplotlib.__version__}\n'
    data_bytes = (ROOT / 'table_export.csv').read_bytes()
    fingerprint = hashlib.sha256(data_bytes).hexdigest()
    text += f'Input SHA-256: {fingerprint}\n'
    OUT.mkdir(exist_ok=True)
    (OUT / 'environment.txt').write_text(text)
