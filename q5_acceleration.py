"""Q5: observed fastest year and least-squares acceleration trend, 2008–2024."""
from analysis_common import OUT, ACC
from analysis_common import load_data, fit, report_fit, save_report, save_plot, save_environment
import numpy as np
import matplotlib.pyplot as plt


def main():
    # 1. Load the CSV.
    df = load_data()
    # 2. Select one fleet average for each year from 2008 through 2024.
    selected = df[(df['Manufacturer'] == 'All') & (df['Vehicle Type'] == 'Sedan/Wagon') &
                  (df['Regulatory Class'] == 'Car') & df['year'].between(2008, 2024)].copy()
    clean = selected.dropna(subset=[ACC]).sort_values('year').copy()
    if clean['year'].duplicated().any() or set(clean['year']) != set(range(2008, 2025)):
        raise ValueError('Expected one complete annual fleet average for each year 2008–2024.')
    # 3. Subtract 2008 so the intercept represents the start of the trend.
    x = clean['year'].to_numpy() - 2008
    model = fit(x, clean[ACC])
    # The fastest year comes from the actual data, not the regression line.
    best = clean[clean[ACC] == clean[ACC].min()]
    clean['fitted time (s)'] = model['predicted']
    clean['residual (s)'] = model['residual']
    OUT.mkdir(exist_ok=True)
    clean[['Model Year', ACC, 'fitted time (s)', 'residual (s)']].to_csv(OUT / 'q5_metrics.csv', index=False)
    # 4. Write the calculated answers to the terminal and a text file.
    fastest_years = []
    for year in best['year']:
        fastest_years.append(str(int(year)))
    year_list = ', '.join(fastest_years)
    text = ('Q5 — Sedan/Wagon annual fleet acceleration, 2008–2024\n'
            f'Selected = {len(selected)}; included = {len(clean)}; missing acceleration = {len(selected)-len(clean)}\n'
            + 'Fastest observed year(s): ' + year_list
            + f'; average 0–60 mph time = {best[ACC].iloc[0]:.4f} s\n'
            + 'Equation: time (s) = intercept + slope × (year − 2008)\n'
            + report_fit('Ordinary least squares', model, len(clean), 's/year')
            + f'Observed 2008 to 2024 change = {clean[ACC].iloc[-1]-clean[ACC].iloc[0]:.4f} s\n'
            + f'Largest absolute residual = {np.abs(model["residual"]).max():.6f} s\n'
            + 'RMSE units: seconds. Lower time means faster acceleration; the fitted trend does not determine the observed minimum.')
    save_report('q5', text)
    # Create and save the graphs using the original formatting.
    fig, axes = plt.subplots(2, 1, figsize=(10, 9), layout='constrained')
    axes[0].plot(clean['year'], clean[ACC], 'o-', label='Reported fleet average', color='#236b8e')
    axes[0].plot(clean['year'], model['predicted'], '--', label='Least-squares trend', color='#cd7533')
    axes[0].scatter(best['year'], best[ACC], s=140, facecolors='none', edgecolors='crimson', linewidths=2, label='Fastest observed year', zorder=4)
    axes[0].set_title('Sedan/Wagon fleet acceleration, 2008–2024')
    axes[0].set_ylabel('Average 0–60 mph time (s)')
    axes[0].set_xlabel('Model year')
    axes[0].legend()
    axes[1].bar(clean['year'], model['residual'], color='#236b8e')
    axes[1].axhline(0, color='black', linewidth=1)
    axes[1].set_title('Residuals from the linear acceleration trend')
    axes[1].set_xlabel('Model year')
    axes[1].set_ylabel('Observed − fitted time (s)')
    for ax in axes:
        ax.set_xticks(range(2008, 2025, 2))
        ax.ticklabel_format(axis='x', style='plain', useOffset=False)
        ax.grid(alpha=.2)
        ax.set_axisbelow(True)
    save_plot(fig, 'q5_acceleration')
    # Record the software versions used to produce these results.
    save_environment()


if __name__ == '__main__':
    main()
