import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
from scipy.integrate import RK45

# Inicial Parameters
V0, T0, P0 = 10, 29.5, 300
alpha, beta, delta, gamma = 0.41, 0.0029, 87.4, 2.967
a, b = 2, 10
mean_temp = 29.5
sigma_T = 2
t_max = 100

# Save series
tempos, biomassa_v, temp_v, prec_v, vc_v = [], [], [], [], []

y0 = [V0, T0, P0]
t0 = 0


# Funtion
def model(t, y):
    V, T, P = y
    Vc = b + P * np.exp(-((T - mean_temp) ** 2) / (2 * sigma_T**2))
    DVdt = a * V * (1 - (V / Vc))
    DTdt = alpha * T - beta * T * P
    DPdt = gamma * T * P - delta * P
    return [DVdt, DTdt, DPdt], Vc


# Plot animation
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
plt.subplots_adjust(bottom=0.4, hspace=0.4)

ax_V, ax_T, ax_P, ax_Vc = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]

(line_V,) = ax_V.plot([], [], color="green", label="Biomass")
(line_T,) = ax_T.plot([], [], color="red", label="Temperature")
(line_P,) = ax_P.plot([], [], color="blue", label="Precipitation")
(line_Vc,) = ax_Vc.plot(
    [], [], color="orange", linestyle="--", label="Carrying capacity"
)

for ax, ylabel in zip(
    [ax_V, ax_T, ax_P, ax_Vc],
    ["Biomass", "Temperature (°C)", "Precipitation (mm/m)", "Carrying capacity"],
):
    ax.set_xlim(0, t_max)
    ax.set_ylim(0, 500)
    ax.set_xlabel("Time (years)")
    ax.set_ylabel(ylabel)
    ax.legend()

# Animation config
ax_alpha = plt.axes([0.15, 0.30, 0.7, 0.03])
slider_alpha = Slider(ax_alpha, "Alpha", 0, 1, valinit=alpha)
ax_beta = plt.axes([0.15, 0.25, 0.7, 0.03])
slider_beta = Slider(ax_beta, "Beta", 0, 0.01, valinit=beta)
ax_delta = plt.axes([0.15, 0.20, 0.7, 0.03])
slider_delta = Slider(ax_delta, "Delta", 0, 5, valinit=gamma)
ax_gamma = plt.axes([0.15, 0.15, 0.7, 0.03])
slider_gamma = Slider(ax_gamma, "Gamma", 0, 100, valinit=delta)
ax_zoom = plt.axes([0.15, 0.10, 0.7, 0.03])
slider_zoom = Slider(ax_zoom, "Zoom Y", 0.5, 5, valinit=1)


# Parameters Control
def update_parameters(val):
    global alpha, beta, delta, gamma, rk
    alpha = slider_alpha.val
    beta = slider_beta.val
    delta = slider_gamma.val
    gamma = slider_delta.val
    # Reinicializa RK45 a partir do estado atual
    rk = RK45(
        fun=lambda t, y: model(t, y)[0],
        t0=tempos[-1] if tempos else t0,
        y0=[
            biomassa_v[-1] if biomassa_v else V0,
            temp_v[-1] if temp_v else T0,
            prec_v[-1] if prec_v else P0,
        ],
        t_bound=t_max,
        max_step=0.1,
    )
    return rk


for s in [slider_alpha, slider_beta, slider_gamma, slider_delta]:
    s.on_changed(update_parameters)

paused = False


def toggle_pause(event):
    global paused
    paused = not paused


ax_pause = plt.axes([0.85, 0.92, 0.1, 0.05])
btn_pause = Button(ax_pause, "Pause/Play")
btn_pause.on_clicked(toggle_pause)


def replay(event):
    global rk, tempos, biomassa_v, temp_v, prec_v, vc_v, paused
    # Resetar variáveis
    tempos = []
    biomassa_v = []
    temp_v = []
    prec_v = []
    vc_v = []
    paused = False

    rk = RK45(
        fun=lambda t, y: model(t, y)[0], t0=t0, y0=y0, t_bound=t_max, max_step=0.1
    )

    for line in [line_V, line_T, line_P, line_Vc]:
        line.set_data([], [])

    for ax, data_init in zip(
        [ax_V, ax_T, ax_P, ax_Vc],
        [
            [V0],
            [T0],
            [P0],
            [b + P0 * np.exp(-((T0 - mean_temp) ** 2) / (2 * sigma_T**2))],
        ],
    ):
        ax.set_xlim(0, t_max)
        ax.set_ylim(0, max(data_init) * 1.2)


ax_replay = plt.axes([0.70, 0.92, 0.1, 0.05])
btn_replay = Button(ax_replay, "Replay")
btn_replay.on_clicked(replay)

# Initialize RK45
rk = RK45(fun=lambda t, y: model(t, y)[0], t0=t0, y0=y0, t_bound=t_max, max_step=0.1)
interval = 0.01

# Main Loop
while rk.t < t_max:
    if not paused:
        rk.step()
        V, T, P = rk.y
        _, Vc = model(rk.t, rk.y)
        tempos.append(rk.t)
        biomassa_v.append(V)
        temp_v.append(T)
        prec_v.append(P)
        vc_v.append(Vc)

        line_V.set_data(tempos, biomassa_v)
        line_T.set_data(tempos, temp_v)
        line_P.set_data(tempos, prec_v)
        line_Vc.set_data(tempos, vc_v)

        zoom_factor = slider_zoom.val
        for ax, data in zip(
            [ax_V, ax_T, ax_P, ax_Vc], [biomassa_v, temp_v, prec_v, vc_v]
        ):
            data_range = max(data) - min(data)
            if data_range == 0:
                data_range = 1
            ax.set_ylim(
                min(data) - 0.1 * data_range,
                min(data) - 0.1 * data_range + zoom_factor * data_range,
            )
            ax.set_xlim(0, max(t_max, rk.t))

        plt.pause(interval)
    else:
        plt.pause(0.1)
