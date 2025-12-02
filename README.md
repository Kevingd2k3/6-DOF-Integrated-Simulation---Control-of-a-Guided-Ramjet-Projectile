# 6-DOF Integrated Simulation and Control of a Guided Ramjet Projectile 

![Python](https://img.shields.io/badge/Code-Python_3.8%2B-blue?logo=python&logoColor=white)
![CFD](https://img.shields.io/badge/Validation-Ansys_Fluent-orange?logo=ansys&logoColor=white)
![Physics](https://img.shields.io/badge/Physics-Supersonic_Aerodynamics-red)
![GNC](https://img.shields.io/badge/Control-Proportional_Navigation-green)
![Status](https://img.shields.io/badge/Status-Complete-success)

## Project Overview

This project establishes a **high-fidelity multi-physics simulation pipeline** designed to optimize the flight dynamics of a supersonic guided projectile.

Moving beyond simple point-mass ballistic estimation, this workflow integrates **Industrial CFD (Ansys Fluent)** for accurate aerodynamic characterization with a custom **Python-based 6-DOF Flight Engine**. The primary objective was to engineer a system capable of a **15 km precision intercept** from a low-altitude launch.

The analysis conclusively demonstrates that standard ballistic trajectories fail due to excessive supersonic wave drag ($C_d \approx 0.67$), validating the necessity of a **Ramjet propulsion system** integrated with **Proportional Navigation (PN)** control logic to achieve the mission profile.

Pictures

![Density Contour](Mach2_Density.png) ![Shockwave](Mach2_Shockwave.png) ![Aerodynamic Data](<Aerodynamic Data From Ansys.png>) ![Turbulent Kinetic Energy](Mach2_TKE.png) ![Ramjet Launched at 2.6 Mach](<Ramjet Projectile w Higher Lauch Velocity .png>) ![Guided Ramjet Tajecotry](<Ramjet Projectile with Thrust.png>) ![Baseline Tamjet](<Ramjet Projectile.png>) ![Pressure Contour](Ramjet_Pressure.png) ![Temperature Contour](Ramjet_Temperature.png)

---

## 📂 Repository Structure

```text
6-DOF INTEGRATED SIMULATION AND CONTROL/
│
├── Ansys/                         # ANSYS Workbench & Fluent Project Files
│   ├── Ramjet_Projectile.wbpj
│   └── ...
│
├── Pictures/                      # Simulation Outputs & Visualization
│   ├── Mach2_Shockwave.png        # CFD: Mach contours showing shock capture
│   ├── Mach2_Density.png          # CFD: Expansion fans visualization
│   ├── Ramjet_Pressure.png        # CFD: Static Pressure distribution
│   ├── Ramjet_Temperature.png     # CFD: Static Temperature distribution
│   ├── Ramjet_Success.png         # Plot: Successful Ramjet Intercept
│   └── Ballistic_Failure.png      # Plot: Failed Ballistic Trajectory
│
├── aerodynamics.csv               # Curated Aerodynamic Database (Mach vs Cd/Cl)
├── main_simulation.py             # MAIN SCRIPT: Ramjet Physics & GNC Loop
├── higher_initial_velocity.py     # Trade Study: The "Big Gun" approach (Failed)
├── projectile_w_thrust.py         # Physics Class definition
└── Report.pdf                     # Full Technical Engineering Report
