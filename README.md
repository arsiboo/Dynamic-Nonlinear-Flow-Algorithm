# A Dynamic Nonlinear Flow Algorithm to Model Patient Flow

**Authors**: Arsineh Boodaghian Asl, Jayanth Raghothama, Adam Darwich, Sebastiaan Meijer  

This repository contains the code for the **dynamic nonlinear flow algorithm** described in our research work. The algorithm simulates hospital patient flows to identify bottlenecks, visualize ward behaviors, and analyze system performance.

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)
- [Input File](#input-file)
- [Output Files](#output-files)
- [Visualization](#visualization)
- [Cite This Work](#cite-this-work)
- [License](#license)
- [Contact](#contact)

---

## Overview
The **Dynamic Nonlinear Flow Algorithm** models patient flows within a hospital system. It accounts for admission, discharge, and transfer rates to simulate ward utilization, overflow, and bottlenecks over time. The project also includes tools for visualizing the results and analyzing hospital performance metrics.

Key features:
- Simulates nonlinear flow of patients between wards.
- Detects and reports bottlenecks.
- Provides visualizations for ward performance and network flows.

---

## Usage
1. **Running the Algorithm**:
   - Use the `main.py` file to run the algorithm.
   - Modify the following lines in `main.py`:
     - Line 9: Specify the dataset file name (input file).
     - Line 61: Indicate the simulation duration in days.


2. **Other Files**:
   - `dynamic_nonlinear_flow_algorithm.py`: Contains the flow algorithm implementation.
   - `dependencies.py`: Provides functions such as the depth-first-search (DFS) algorithm.



## Input File
mini-hospital.xlsx sheets:

- **vertices**: List of hospital wards with corresponding number of beds and staff.
- **edges**: List of care pathways connecting the wards with corresponding edge capacity and distribution probability.
- **arrival_rate**: List of arrival rates per unit time.
- **service_time**: List of different service times per ward.
- **mini-hospital-fitter (Folder)**: Contains distribution functions per ward.

## Outputs and Visualization
- **minmax_graph.xlsx** output file contains the data to visualize the persistency using **persistency.py**, visualize the severity using **severity.py**, and visualize the overflow using **overflow.py**.
- **paths.xlsx**

## 

