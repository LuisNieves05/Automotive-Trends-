# Automotive Trends

ENGR 315 — Semester Project

## Team Name and Contributors

**Team:** Python Warriors  
**Contributors:** Van Lawler and Luis Nieves

## Objective and Motivation

This project will use EPA Automotive Trends data to compare fuel economy across vehicle classifications, examine the relationship between horsepower and fuel economy, and identify the model year with the fastest average Sedan/Wagon acceleration. Least-squares fitting will be used for the horsepower and acceleration questions.

Our shared interest in automotive systems and engineering motivated this project. We first worked together on an autonomous vehicle in ENGR 112 under Dr. Gipson and successfully accomplished our objectives. As seniors, we chose this project to revisit that interest and deepen our understanding of the automotive industry.

### Dataset

The source is the [EPA Automotive Trends dataset](https://www.epa.gov/automotive-trends/explore-automotive-trends-data), which can be explored online or exported as a CSV. EPA uses manufacturer-submitted data received through its regulatory programs. The repository's `table_export.csv` contains 5,661 records and 57 columns, with model-year labels from 1975 through 2024 and a separate `Prelim. 2025` label. The planned analyses use finalized model years through 2024, following the Phase 0 proposal.

The relevant fields are:

| Field | Use |
| --- | --- |
| `Manufacturer`, `Model Year` | Select manufacturer groups and analysis years. |
| `Regulatory Class`, `Vehicle Type` | Define comparable vehicle groups and avoid overlapping categories. |
| `Real-World MPG` | Primary fuel-economy measure, in miles per gallon. |
| `Real-World MPG_City`, `Real-World MPG_Hwy` | Optional city/highway comparisons, kept separate from combined MPG. |
| `Horsepower (HP)` | Explanatory variable for the horsepower–fuel-economy fit. |
| `Acceleration (0-60 time in seconds)` | Acceleration measure; a lower value means faster acceleration. |
| `Production (000)`, `Production Share` | Production context and weights for the manufacturer regression. |
| Powertrain share columns | Examine the possible influence of BEVs, plug-in hybrids, and other hybrids. |

### Selected Questions, Expected Answer Forms, and Benefits

The question numbers below retain the numbering from the proposal. All numerical expectations are **preliminary values reported in Phase 0**, to be reproduced and checked in later phases.

| Question | Expected answer form | Potential benefit |
| --- | --- | --- |
| **Q2. How significantly does fuel economy vary between different vehicle classifications?** | A table and bar chart of 2024 real-world MPG for five non-overlapping vehicle types, with absolute MPG differences and percentage differences relative to a stated baseline. The proposal reports an expected cars/SUVs-versus-pickups difference of 18.64 MPG (90.7%); the exact cars/SUVs grouping and averaging rule must be documented when reproducing it. | Show the size of fuel-economy differences among vehicle types and support informed comparisons. |
| **Q4. What is the relationship between engine horsepower and fuel efficiency?** | Unweighted and production-weighted linear equations, slopes, R², RMSE, and diagnostic plots for 2024 Sedan/Wagon averages across 14 manufacturer groups. The proposal's preliminary unweighted fit is MPG = 15.22 + 0.0917(HP), with R² = 0.116 and RMSE = 23.00 MPG. | Assess how well horsepower alone describes fuel economy across a fleet with mixed powertrains. |
| **Q5. Which year produced the fastest average 0–60 mph cars?** | The year with the lowest reported annual Sedan/Wagon average time during 2008–2024, plus a fitted trend, slope, R², RMSE, and residual plot. The proposal identifies 2023 at 7.4135 s and a preliminary trend of −0.07927 s/year, R² = 0.927, and RMSE = 0.109 s. | Quantify changes in average acceleration and identify the fastest year within the selected period. |

## Introduction / Context of the Project

The CSV contains aggregate fleet and manufacturer records, rather than independent observations for individual cars. It includes both broad totals (`All`, `All Car`, and `All Truck`) and narrower vehicle types. Mixing these levels would double-count groups. The five non-overlapping types used for Q2 are Sedan/Wagon, Car SUV, Truck SUV, Minivan/Van, and Pickup.

For Q4 and Q5, “cars” refers specifically to Sedan/Wagon, matching the proposal. Relationships among aggregate averages do not establish vehicle-level relationships or causation. Powertrain mix, production volume, and other vehicle characteristics can influence the comparisons. Q2 addresses the magnitude of observed differences; aggregate class averages alone do not support a vehicle-level statistical significance test.

The selected scope is Q2, Q4, and Q5. The proposal deferred the CO₂ questions because the chosen export lacked a CO₂ field; the manufacturer acceleration question was considered but not selected.

## Implementation Details

The following describes the **planned implementation**. The repository currently contains the data and report; `script.py` is an empty starting point.

### Tools and Data Preparation

- **Python and pandas:** import the CSV, select records, clean fields, and produce comparison tables.
- **NumPy:** calculate differences, fit ordinary and weighted least-squares models, and compute model metrics.
- **Matplotlib:** create labeled comparison, regression, time-series, and residual plots. VS Code will be used for development.
- Preserve `table_export.csv` as the source export. Record its source, export filters, retrieval date, and the Python/package versions when implementing the analysis.
- Treat `-` and blank numeric cells as missing, convert numeric fields explicitly, and exclude `Prelim. 2025`. Remove missing values only for fields required by each analysis, recording the excluded counts.
- Select a single aggregation level for each question. Check uniqueness by manufacturer, year, regulatory class, and vehicle type. Do not mix `Manufacturer = All` totals with individual manufacturer rows in the same fit.
- Keep combined, city, highway, and 2-cycle MPG measures distinct. Inspect unusual observations and powertrain shares before deciding whether any exclusion is justified; document all exclusions.

### Q2 — Fuel Economy by Vehicle Classification

1. Filter to model year 2024 and `Manufacturer = All`. Select the five non-overlapping vehicle types and their matching regulatory classes: Sedan/Wagon and Car SUV are `Car`; Truck SUV, Minivan/Van, and Pickup are `Truck`.
2. Use each selected EPA aggregate's `Real-World MPG` directly. Report a comparison table and identify the highest and lowest values.
3. For class MPG value M and pickup baseline P, calculate the absolute difference as M − P and the percentage difference as 100 × (M − P) / P. State the baseline beside every percentage. If reproducing the proposal's combined cars/SUVs comparison, specify which types it includes and whether its average is weighted; do not treat overlapping total rows as additional types.
4. Produce a bar chart of MPG by vehicle type and a table of absolute and percentage differences. Discuss potential explanations as hypotheses, including powertrain and vehicle characteristics.

### Q4 — Horsepower Versus Fuel Economy

1. Filter to 2024, `Vehicle Type = Sedan/Wagon`, and `Regulatory Class = Car`. Exclude `Manufacturer = All`, retain complete horsepower–MPG pairs, and verify the proposal's 14 manufacturer groups.
2. Fit MPG = a + b × HP by ordinary least squares, minimizing the sum of squared MPG residuals. Each manufacturer group receives equal weight.
3. Fit the same equation using positive `Production (000)` values as weights, minimizing the sum of production-weighted squared residuals. Normalize weights if needed; this does not change the coefficients. Compare both fits on the same eligible groups.
4. Report intercept, slope in MPG/HP, sample count, R², and RMSE in MPG for each fit. For weighted metrics, use the weighted mean and weighted sums consistently and label them separately from unweighted metrics.
5. Plot MPG against HP with manufacturer labels and both fitted lines. Add residual-versus-HP or residual-versus-fitted plots. Examine BEV and hybrid shares where available to assess whether powertrain mix helps explain influential observations; label any subset fit separately.

The positive preliminary slope and low R² in the proposal are a reason to inspect the mixed-powertrain data carefully. They do not establish that increasing a vehicle's horsepower improves its fuel economy.

### Q5 — Acceleration Trends by Model Year

1. Filter to `Manufacturer = All`, `Vehicle Type = Sedan/Wagon`, `Regulatory Class = Car`, and model years 2008–2024. Use one reported fleet-average acceleration value per year and verify coverage of all 17 years.
2. Identify the minimum observed 0–60 mph time and report its year and time, including ties if present. The fastest observed year is determined from the data, independently of the fitted line.
3. Fit time = a + b × (year − 2008) by ordinary least squares. Centering the year makes the intercept easier to interpret while retaining slope units of seconds/year.
4. Report slope, intercept, sample count, R², and RMSE in seconds. Plot annual times with the fitted trend and highlight the observed minimum. Plot residuals against year to inspect curvature, unusual years, and remaining time patterns.
5. Interpret a negative slope as shorter average acceleration times over the selected period. Discuss changing fleet composition and powertrain technology as possible influences without claiming causation or extrapolating beyond the study period.

### Metrics and Later-Phase Documentation

For unweighted fits, residuals are observed values minus fitted values. RMSE = sqrt(sum(residual²) / n), and R² = 1 − sum(residual²) / sum((observed − mean(observed))²). Weighted versions use production weights in both the error sums and the mean, with RMSE divided by the sum of weights.

In coming phases, add the completed analysis code, reproducible run instructions and dependencies, saved tables and plots, and relevant screenshots. Include a workflow/block diagram, top-level code overview, or short method-specific code excerpts where they help explain the implementation. Link those artifacts here once they exist.

## Results (Answers to the Questions)

## Conclusions

## Actions that Need to Be Completed

## References / Source Files

1. Lawler, Van, and Luis Nieves. [ENGR 315 Project Proposal Phase 0](https://docs.google.com/document/d/1lZWqDVpIDsLwhNl9FWUNwnT43zpCnR5gD58CyNgnr3M/edit). Source of the project scope, selected questions, and preliminary expectations.
2. U.S. Environmental Protection Agency. [Explore the Automotive Trends Data](https://www.epa.gov/automotive-trends/explore-automotive-trends-data). Dataset portal; accessed October 28, 2026. The portal is updated over time; retain the repository export and document its provenance for reproducibility.
3. U.S. Environmental Protection Agency. [The 2024 EPA Automotive Trends Report Executive Summary](https://nepis.epa.gov/Exe/ZyPDF.cgi?Dockey=P101CUZD.pdf). Reference cited in the proposal, accessed there on October 19, 2026.
4. [`table_export.csv`](table_export.csv) — EPA data export currently included in this repository.
5. [`Full Report Publication.pdf`](Full%20Report%20Publication.pdf) — report file currently included in this repository.
6. [`script.py`](script.py) — empty starter file reserved for the analysis implementation.
7. [Automotive Trends GitHub repository](https://github.com/LuisNieves05/Automotive-Trends-) — project source repository.
