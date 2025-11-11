# Climate-Biomass Simulation

This project is based on my master's thesis (Dynamical System Modeling of the Influence of Climate Change on Biomass Indicators in the Amazon). The idea is to simulate biomass and its response to perturbations in the climatic patterns of the Amazon region.

The simulation implements a **Lotka-Volterra-inspired model** for climate variables:

- **Temperature (T)** acts like a "prey".
- **Precipitation (P)** acts like a "predator".
- **Biomass (V)** grows logistically, with a carrying capacity \(V_c\) that depends on T and P.

## Model Equations

The system of differential equations is:

$$\frac{dV}{dt} = a \, V \left(1 - \frac{V}{V_c}\right)$$

$$V_c = V_\text{min} + b \, P \, \exp\left(-\frac{(T - T_\text{opt})^2}{2 \sigma_T^2}\right)$$

$$\frac{dT}{dt} = \alpha T - \beta T P$$

$$\frac{dP}{dt} = \gamma T P - \delta P$$

Where:

- $$\( \alpha, \beta, \gamma, \delta \)$$ are positive adjustable parameters.
- $$\( V_c \)$$ represents the carrying capacity for biomass.
- $$\( \sigma_T \)$$ defines thermal tolerance for plants.
- $$\( a \)$$ is the biomass growth rate.
- $$\( b \)$$ adjusts the influence of precipitation on $$\( V_c \)$$.

## Concept and Motivation

### Carrying Capacity $$\(V_c\)$$

- $$\(V_c\)$$ depends directly on **precipitation** $$\(P\)$$ and **temperature** $$\(T\)$$.
- Precipitation increases the carrying capacity: more water availability allows higher biomass.
- Temperature affects $$\(V_c\)$$ through a **thermal tolerance function**:
  - $$\(V_c\)$$ decreases when $$\(T\)$$ deviates from the optimal temperature $$\(T_\text{opt}\)$$.
  - This reflects plant physiological limits: growth is maximal at moderate temperatures and declines under thermal stress.
- Mathematically, this is represented by a Gaussian-like term in the equation for $$\(V_c\)$$, where the peak corresponds to the optimal temperature and the width $$(\(\sigma_T\))$$ represents tolerance.

### Biomass Response

- Biomass grows logistically up to $$\(V_c\)$$.
- Changes in precipitation rapidly modify $$\(V_c\)$$, representing **sudden water availability shifts**.
- Temperature deviations reduce $$\(V_c\)$$, capturing the effect of **thermal stress** on plant growth and survival.
- The interplay between P and T can lead to **phase-shifted oscillations**, similar to predator-prey cycles in Lotka-Volterra dynamics, but applied to climate-biomass interactions.


## Implementation

- Implemented in **Python** using **RK45** (5th-order Runge-Kutta) for numerical integration.
- Generates animated plots of:
  - Biomass
  - Temperature
  - Precipitation
  - Carrying capacity
- Includes interactive controls to:
  - Adjust parameters $$\(\alpha, \beta, \gamma, \delta\)$$
  - Pause/restart the simulation
  - Zoom in/out on graphs

## Perturbations

- The model allows simulating extreme events, e.g.:
  - A 20% increase in $$\(\delta\)$$ between years 20–21, representing abrupt precipitation changes.
- This feature allows studying **biomass resilience under climate disturbances**.

## References

- Lotka, A. J. (1925). *Elements of Physical Biology*.
- Volterra, V. (1926). *Fluctuations in the abundance of a species considered mathematically*.
- Anisiu, 2014. Predator-prey dynamics studies.
- Schulze et al., 2019. Effects of temperature and water on plant physiological processes.
- Sanchez-Martinez et al., 2025. Impact of precipitation on Amazon biomass.
- Marengo et al., 2024. Climate disturbances and forest resilience.

---

**Note:** This is a simplified model designed to capture general climate-biomass interaction patterns in the Amazon.

