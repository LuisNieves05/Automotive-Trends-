"""Q4: ordinary and production-weighted fits of 2024 manufacturer MPG on HP."""
from analysis_common import OUT, MPG, HP, PROD
from analysis_common import load_data, fit, report_fit, save_report, save_plot, save_environment
import numpy as np
import matplotlib.pyplot as plt


def main():
    # 1. Load the CSV.
    df = load_data()
    # 2. Select only 2024 Sedan/Wagon manufacturer averages.
    selected = df[(df['year'] == 2024) & (df['Vehicle Type'] == 'Sedan/Wagon') &
                  (df['Regulatory Class'] == 'Car') & (df['Manufacturer'] != 'All')].copy()
    if selected['Manufacturer'].duplicated().any():
        raise ValueError('Duplicate manufacturer groups.')
    clean = selected.dropna(subset=[HP, MPG, PROD])
    clean = clean[clean[PROD] > 0].sort_values('Manufacturer').copy()
    # 3. Calculate both fits on the same complete manufacturer rows.
    ordinary = fit(clean[HP], clean[MPG])
    weighted = fit(clean[HP], clean[MPG], clean[PROD])
    # 4. Build the printed report, including a separate Tesla sensitivity check.
    text = ('Q4 — 2024 Sedan/Wagon manufacturer averages\n'
            f'Selected = {len(selected)}; included = {len(clean)}; excluded missing/nonpositive production = {len(selected)-len(clean)}\n'
            'Equation: MPG = intercept + slope × HP\n'
            + report_fit('Ordinary least squares (equal manufacturer weight)', ordinary, len(clean), 'MPG/HP')
            + report_fit('Production-weighted least squares (weighted R² and RMSE)', weighted, len(clean), 'MPG/HP')
            + 'RMSE units: MPG. Metrics are in-sample descriptive fit measures, not held-out prediction scores.\n')
    # Explicitly labeled sensitivity analysis; keep Tesla in the primary fits.
    without = clean[clean['Manufacturer'] != 'Tesla']
    if len(without) >= 3 and len(without) != len(clean):
        text += report_fit('Sensitivity only: ordinary fit excluding Tesla', fit(without[HP], without[MPG]), len(without), 'MPG/HP')
    # Keep the powertrain columns in the saved table for later investigation.
    share_cols = []
    for column in clean.columns:
        is_powertrain = column.startswith('Powertrain -')
        is_electrified = 'BEV' in column or 'PHEV' in column or 'HEV' in column
        if is_powertrain and is_electrified:
            share_cols.append(column)

    clean['ordinary fitted MPG'] = ordinary['predicted']
    clean['ordinary residual MPG'] = ordinary['residual']
    clean['weighted fitted MPG'] = weighted['predicted']
    clean['weighted residual MPG'] = weighted['residual']
    OUT.mkdir(exist_ok=True)
    clean[['Manufacturer', HP, MPG, PROD] + share_cols + ['ordinary fitted MPG', 'ordinary residual MPG', 'weighted fitted MPG', 'weighted residual MPG']].to_csv(OUT / 'q4_metrics.csv', index=False)
    save_report('q4', text)
    # Create and save the graphs using the original formatting.
    fig, axes = plt.subplots(2, 1, figsize=(11, 10), layout='constrained')
    ax = axes[0]
    ax.scatter(clean[HP], clean[MPG], s=45, color='#236b8e')
    # Spread labels around the dense low-horsepower cluster; leader lines identify points.
    offsets = {'Honda': (-55, 35), 'Nissan': (-15, 58), 'Hyundai': (20, 76),
               'Toyota': (35, 38), 'Kia': (-40, 10), 'Mazda': (30, -2),
               'Subaru': (-50, -35), 'GM': (25, -45)}
    for _, row in clean.iterrows():
        offset = offsets.get(row['Manufacturer'], (6, 8))
        ax.annotate(row['Manufacturer'], (row[HP], row[MPG]), xytext=offset,
                    textcoords='offset points', fontsize=8,
                    arrowprops=dict(arrowstyle='-', color='gray', lw=.6))
    grid = np.linspace(clean[HP].min()-15, clean[HP].max()+20, 100)
    ordinary_line = ordinary['intercept'] + ordinary['slope'] * grid
    weighted_line = weighted['intercept'] + weighted['slope'] * grid
    ordinary_label = f'Ordinary: R²={ordinary["r2"]:.3f}, RMSE={ordinary["rmse"]:.2f} MPG'
    weighted_label = f'Production-weighted: R²={weighted["r2"]:.3f}, RMSE={weighted["rmse"]:.2f} MPG'
    ax.plot(grid, ordinary_line, '-', label=ordinary_label)
    ax.plot(grid, weighted_line, '--', label=weighted_label)
    ax.set_title('2024 Sedan/Wagon: horsepower and fuel economy by manufacturer')
    ax.set_xlabel('Average horsepower (HP)')
    ax.set_ylabel('Real-world fuel economy (MPG)')
    ax.margins(x=.15, y=.15)
    ax.legend(fontsize=9)
    axes[1].scatter(clean[HP], ordinary['residual'], label='Ordinary', marker='o')
    axes[1].scatter(clean[HP], weighted['residual'], label='Production-weighted', marker='x')
    axes[1].axhline(0, color='black', linewidth=1)
    axes[1].set_title('Regression residuals')
    axes[1].set_xlabel('Average horsepower (HP)')
    axes[1].set_ylabel('Observed − fitted MPG')
    axes[1].legend()
    axes[0].grid(alpha=.2)
    axes[1].grid(alpha=.2)
    save_plot(fig, 'q4_horsepower')
    # Record the software versions used to produce these results.
    save_environment()


if __name__ == '__main__':
    main()
