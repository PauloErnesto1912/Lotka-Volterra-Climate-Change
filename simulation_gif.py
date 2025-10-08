import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import RK45

# Inicial Parameters
V0, T0, P0 = 10, 29.5, 300
a, b = 2, 10
mean_temp = 29.5
sigma_T = 2
c = 1.17
alpha0 = 0.350872425 * c
beta = 0.00251599122 * c
gamma = 2.96707914 * c
delta = 87.4030685 * c
t_max = 40


# Model with disturbance in gamma
def model(t, y):
    V, T, P = y
    gamma_curr = gamma
    if 20 <= t <= 21:
        gamma_curr *= 1.2  # +20%
    Vc = b + P * np.exp(-((T - mean_temp) ** 2) / (2 * sigma_T**2))
    DVdt = a * V * (1 - V / Vc)
    DTdt = alpha0 * T - beta * T * P
    DPdt = gamma_curr * T * P - delta * P
    return [DVdt, DTdt, DPdt], Vc


# Calc RK45
y0 = [V0, T0, P0]
tempos, biomassa_v, temp_v, prec_v, vc_v = [], [], [], [], []

rk = RK45(fun=lambda t, y: model(t, y)[0], t0=0, y0=y0, t_bound=t_max, max_step=0.01)
while rk.t < t_max:
    rk.step()
    V, T, P = rk.y
    _, Vc = model(rk.t, rk.y)
    tempos.append(rk.t)
    biomassa_v.append(V)
    temp_v.append(T)
    prec_v.append(P)
    vc_v.append(Vc)

tempos = np.array(tempos)
biomassa_v = np.array(biomassa_v)
temp_v = np.array(temp_v)
prec_v = np.array(prec_v)
vc_v = np.array(vc_v)

N_frames = 300
indices = np.linspace(0, len(tempos) - 1, N_frames, dtype=int)

tempos_gif = tempos[indices]
biomassa_gif = biomassa_v[indices]
temp_gif = temp_v[indices]
prec_gif = prec_v[indices]
vc_gif = vc_v[indices]

fig, axs = plt.subplots(2, 2, figsize=(10, 6))
ax_V, ax_T, ax_P, ax_Vc = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]

lines = []
for ax, data, label, color in zip(
    [ax_V, ax_T, ax_P, ax_Vc],
    [biomassa_gif, temp_gif, prec_gif, vc_gif],
    ["Biomassa", "Temperatura", "Precipitação", "Capacidade de Suporte"],
    ["green", "red", "blue", "orange"],
):
    (line,) = ax.plot([], [], color=color, label=label)
    ax.set_xlim(0, t_max)
    ax.set_ylim(0, max(data) * 1.1)  # Limite Y individual, 10% acima do máximo
    ax.set_xlabel("Tempo (anos)")
    ax.set_ylabel(label)
    ax.legend()
    lines.append(line)


# Animation
def animate(i):
    for line, data in zip(lines, [biomassa_gif, temp_gif, prec_gif, vc_gif]):
        line.set_data(tempos_gif[:i], data[:i])
    return lines


frames = len(tempos_gif)
interval = 10000 / frames

ani = FuncAnimation(fig, animate, frames=frames, interval=interval, blit=True)
writer = PillowWriter(fps=30)
ani.save("simulacao_perturbacao.gif", writer=writer)
print("GIF salvo como 'simulacao_perturbacao.gif'")
