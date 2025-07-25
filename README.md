# A Dynamic Nonlinear Flow Algorithm to Model Patient Flow

This repository contains the code for the **dynamic nonlinear flow algorithm** described in the following research paper. The algorithm simulates hospital patient flows to identify bottlenecks, analyze ward behavior, and evaluate system performance.

> **Note:** This research was conducted as part of my PhD studies at KTH Royal Institute of Technology.

---

## Citation

If you use this algorithm in your research or publications, please cite the following work:

Boodaghian Asl, A., Raghothama, J., Darwich, A. S., & Meijer, S. (2025).
*A dynamic nonlinear flow algorithm to model patient flow.*  
Scientific Reports, 15(1), 12052
[Read the Paper](https://www.nature.com/articles/s41598-025-96536-z)

---

## Usage

### 1. Running the Algorithm
- Run the simulation via `main.py`. The script includes step-by-step comments.
- Modify the following lines:
  - **Line 9**: Specify the dataset file name (Excel format).
  - **Line 61**: Set the simulation duration (in days).

### 2. Code Structure
- **`dynamic_nonlinear_flow_algorithm.py`** — Implements the core algorithm.
- **`dependencies.py`** — Contains utility functions such as depth-first search (DFS).

---

## Input Files

The model requires an Excel file and a folder structured as follows:

- **`vertices` sheet** — List of hospital wards with number of beds and staff.
- **`edges` sheet** — Care pathways between wards with edge capacities and probabilities.
- **`arrival_rate` sheet** — Patient arrival rates over time.
- **`service_time` sheet** — Service time distributions for each ward.
- **`mini-hospital-fitter/` folder** — Pre-fitted distribution functions for service times.

---

## Outputs and Visualization

- **`minmax_graph.xlsx`** — Used to visualize:
  - *Persistency* with `persistency.py`
  - *Severity* with `severity.py`
  - *Overflow* with `overflow.py`

- **`paths.xlsx`** — Patient flow network data, visualized using `network_visualization.py`.

- **`wards_behaviour.csv`** — Ward activity over time, visualized using `line_chart.py`.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Related Work

- [A Hybrid Approach to Model Hospitals and Evaluate Wards' Performances](https://github.com/arsiboo/Agent-Based-Network-Simulation-Combined-Network-Algorithm)

