# A Dynamic Nonlinear Flow Algorithm to Model Patient Flow

**Authors**: Arsineh Boodaghian Asl, Jayanth Raghothama, Adam S. Darwich, Sebastiaan Meijer  

This repository contains the code for the **dynamic nonlinear flow algorithm** described in our research. The algorithm simulates hospital patient flows to identify bottlenecks, analyze ward behaviors, and evaluate system performance.

If you use this algorithm in your research or publications, you are **required to cite** this work as follows:

Paper link: https://www.nature.com/articles/s41598-025-96536-z

**Citation**
Boodaghian Asl, A., Raghothama, J., Darwich, A. S., & Meijer, S. (2025). *A dynamic nonlinear flow algorithm to model patient flow*. *Scientific Reports*. https://doi.org/10.1038/s41598-025-96536-z

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Usage
1. **Running the Algorithm**:
   - Use the `main.py` file to run the algorithm. The file has step by step comments.
   - Modify the following lines in `main.py`:
     - Line 9: Specify the file name for the dataset.
     - Line 61: Indicate the simulation duration in days.

---

2. **Other Files**:
   - `dynamic_nonlinear_flow_algorithm.py`: Contains the flow algorithm implementation.
   - `dependencies.py`: Provides functions such as the depth-first-search (DFS) algorithm.

---
  
## Input File
mini-hospital.xlsx sheets and folder:

- **vertices**: List of hospital wards with corresponding number of beds and staff.
- **edges**: List of care pathways connecting the wards with corresponding edge capacity and distribution probability.
- **arrival_rate**: List of arrival rates per unit time.
- **service_time**: List of different service times per ward, derived from distribution functions.
- **mini-hospital-fitter (Folder)**: Contains distribution functions per ward.

---

## Outputs and Visualization
- **minmax_graph.xlsx** contains the data to visualize the persistency using **persistency.py**, visualize the severity using **severity.py**, and visualize the overflow using **overflow.py**.
- **paths.xlsx** contains the data to visualize the patient flow network using **network_visualization.py**.
- **wards_behaviour.csv** output file contains the data to visualize the wards behaviour over time using **line_chart.py**


