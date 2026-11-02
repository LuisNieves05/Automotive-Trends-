"""Q2: compare finalized 2024 vehicle-type MPG; run with python q2_vehicle_classes.py."""
from analysis_common import OUT, MPG, load_data, save_report, save_plot, save_environment
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # 1. Load the CSV.
    df = load_data()
    # 2. Keep 2024 totals and the five vehicle types in the chart order.
    vehicle_types = ['Sedan/Wagon', 'Car SUV', 'Truck SUV', 'Minivan/Van', 'Pickup']
    regulatory_classes = ['Car', 'Car', 'Truck', 'Truck', 'Truck']
    selected_rows = []
    for i in range(len(vehicle_types)):
        matches = df[(df['year'] == 2024) & (df['Manufacturer'] == 'All') &
                     (df['Vehicle Type'] == vehicle_types[i]) &
                     (df['Regulatory Class'] == regulatory_classes[i])]
        if len(matches) != 1:
            raise ValueError('Expected one total row for each vehicle type.')
        selected_rows.append(matches)

    # Join the five one-row tables together in the same order.
    selected = pd.concat(selected_rows, ignore_index=True)
    missing = int(selected[MPG].isna().sum())
    if missing > 0:
        raise ValueError(f'{missing} required class MPG values are missing.')

    # 3. Calculate differences using pickups as the baseline.
    baseline = float(selected.loc[selected['Vehicle Type'] == 'Pickup', MPG].iloc[0])
    selected['Difference vs pickup (MPG)'] = selected[MPG] - baseline
    selected['Difference vs pickup (%)'] = 100 * (selected[MPG] - baseline) / baseline
    table = selected[['Vehicle Type', MPG, 'Difference vs pickup (MPG)', 'Difference vs pickup (%)']]
    OUT.mkdir(exist_ok=True)
    table.to_csv(OUT / 'q2_metrics.csv', index=False)
    top = selected.loc[selected[MPG].idxmax()]
    # This explicitly defined descriptive average is not a combined fleet MPG.
    cars_suvs = selected[selected['Vehicle Type'].isin(['Sedan/Wagon', 'Car SUV', 'Truck SUV'])][MPG].mean()
    # 4. Build the printed report.
    text = ('Q2 — 2024 real-world MPG by vehicle type\n'
            f'Included = {len(table)} aggregate rows; missing required values = {missing}\n'
            + table.to_string(index=False, float_format=lambda v: f'{v:.5f}')
            + f'\nHighest MPG: {top["Vehicle Type"]} ({top[MPG]:.5f} MPG)'
            + f'\nPickup baseline: {baseline:.5f} MPG'
            + f'\nEqual-type mean of Sedan/Wagon, Car SUV, Truck SUV: {cars_suvs:.5f} MPG'
            + f'\nThat mean minus pickup: {cars_suvs-baseline:.5f} MPG ({100*(cars_suvs-baseline)/baseline:.5f}%)'
            + '\nThis equal-type mean is descriptive, not a production-weighted fleet MPG. No significance test is inferred from aggregate averages.')
    save_report('q2', text)
    # Create and save the graphs using the original formatting.
    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
    colors = ['#236b8e', '#236b8e', '#236b8e', '#236b8e', '#cd7533']
    bars = ax.bar(table['Vehicle Type'], table[MPG], color=colors)
    ax.bar_label(bars, fmt='%.2f', padding=4)
    ax.set_title('2024 fuel economy across five vehicle types')
    ax.set_ylabel('Real-world fuel economy (MPG)')
    ax.set_xlabel('EPA vehicle type')
    ax.set_ylim(0, table[MPG].max()*1.16)
    ax.grid(axis='y', alpha=.2)
    ax.set_axisbelow(True)
    save_plot(fig, 'q2_vehicle_classes')
    # Record the software versions used to produce these results.
    save_environment()


if __name__ == '__main__':
    main()
