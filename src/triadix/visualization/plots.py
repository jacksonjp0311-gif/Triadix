import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path


def generate_plots(chain, run_root: str) -> None:
    vis_dir = Path(run_root) / "visuals"
    vis_dir.mkdir(parents=True, exist_ok=True)

    E = [b.E for b in chain]
    I = [b.I for b in chain]
    D = [b.dphi for b in chain]
    C = [b.C for b in chain]

    def plot(series, title, name):
        fig = plt.figure(figsize=(7, 3), dpi=160)
        ax = plt.gca()
        ax.plot(series, linewidth=1.1)
        ax.set_title(title)
        ax.grid(alpha=0.2)
        fig.tight_layout(pad=0.35)
        fig.savefig(vis_dir / name, bbox_inches="tight", pad_inches=0.06)
        plt.close(fig)

    plot(E, "Entropy E_n", "E.png")
    plot(I, "Entropy I_n", "I.png")
    plot(D, "Phase Drift DeltaPhi_n", "dphi.png")
    plot(C, "Coherence C_n", "C.png")