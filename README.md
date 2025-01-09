# A Dynamic Nonlinear Flow Algorithm to Model Patient Flow

**Authors**: Arsineh Boodaghian Asl, Jayanth Raghothama, Adam Darwich, Sebastiaan Meijer  

This repository contains the code for the **dynamic nonlinear flow algorithm** described in our research work.

## Table of Contents
- [Usage](#usage)
- [Cite This Work](#cite-this-work)
- [License](#license)
- [Contact](#contact)

## Usage

1. **Running the Algorithm**:
   - Use the `main.py` file to run the algorithm.
     - Line 9: Indicate the dataset file name.
     - Line 61: Indicate the duration (in days) for the simulation.

2. **Other Files**:
   - `dynamic_nonlinear_flow_algorithm.py`: Contains the modified flow algorithm code.
   - `dependencies.py`: Contains utility functions for the depth-first-search (DFS) algorithm and other utilities.

3. **Visualization Files**:
   - `line_chart.py`: Visualizes the behavior of wards over time.
   - `network_visualization.py`: Visualizes the network of patient flows.
   - `persistency.py`: Visualizes the persistency of bottlenecks.
   - `severity.py`: Visualizes the severity of bottlenecks.
   - `overflow.py`: Visualizes ward overflow.

## Cite This Work

If you use this code in your research, please cite our work using the following **temporary DOI** until the final DOI is issued upon publication:  
[![DOI](https://zenodo.org/badge/DOI/10.xxxx/temporary-doi.svg)](https://doi.org/10.xxxx/temporary-doi)

**Note:** The DOI will be updated after the paper is published in *Scientific Reports*. Please check this repository for the final DOI.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or feedback, please feel free to contact us at:  
- **Arsineh Boodaghian Asl**: arsineh@kth.se  
- **Jayanth Raghothama**: jayanthr@kth.se
- **Adam Darwich**: darwich@kth.se  
- **Sebastiaan Meijer**: smeijer@kth.se
