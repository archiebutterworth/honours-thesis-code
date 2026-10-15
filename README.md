# Quantum State Preparation and Certification for Large-Scale Classical Data

Code and data accompanying the BPhil (Hons) thesis of the same name.

**Archie Butterworth** — Supervisor: Prof. Jingbo Wang
School of Physics, Mathematics and Computing, The University of Western Australia, 2026

The thesis has two halves, and so does this repository:

- **Chapter 4** — Schmidt Spectrum Optimisation (SSO) state preparation of a 13-qubit
  acoustic signal on Quantinuum's H2-1 trapped-ion quantum computer, certified with
  shadow overlap, plus the **τ reducing layer**: a pre-measurement basis change that
  minimises the inverse participation ratio (IPR) as a tractable surrogate for the
  certification parameter τ.
- **Chapter 5** — **Q-MERGE**, a state-preparation framework that partitions a large
  target state into *M* *n*-qubit segments, prepares them independently and in
  parallel, and merges them onto one register using SELECT-SWAP operations and
  measurement.

Every figure in the thesis that comes from code can be regenerated from what is in
here. Long-running results (SSO sweeps that take CPU-hours, and all Quantinuum
hardware shots, which cannot be re-run without machine time) are committed as raw
data files so the plotting notebooks run immediately.

---

## Quick start

```bash
pip install -r requirements.txt
```

Then run the notebooks **with their own directory as the working directory** — they
resolve all paths relative to `os.getcwd()`:

```bash
cd chapter5_qmerge && jupyter lab 04_figures.ipynb
```

Developed against Python 3.11. `requirements.txt` pins the exact versions used for
the thesis results; see the note at the top of that file about optimiser drift.

---

## Repository layout

### `chapter4_certification/`

| Notebook | Purpose |
|---|---|
| `00_sso_chi4_disentangler.ipynb` | SSO with the χ=4 disentangler (exploratory) |
| `01_sso_preparation.ipynb` | The SSO/MPS state-preparation stack |
| `02_tau_reducing_layer.ipynb` | IPR optimiser; builds the structured test states (sinusoidal wave packets, 1D MBL, 1D spinless Hubbard, 4×4 2D Heisenberg) and writes `tau_ipr_{before,after}.npy` |
| `03_hardware_analysis.ipynb` | Compares noiseless / H2-1 emulator / H2-1 hardware shadow overlaps |
| `04_tket_compilation.ipynb` | Compiles to the H2-1 native gate set (229 × 1-qubit `PhasedX`, 108 × 2-qubit `ZZPhase`) |
| `05_figures.ipynb` | **Produces Figures 4.1–4.5** |

Data in the same directory: `shadow_results_{hardware,emulator}.pkl`,
`shadow_results_noiseless.npy`, `shadows_vs_fidelity.npy`,
`tau_ipr_{before,after}.npy`, `taued_target_state.npy`, `Jies_Acoustic_Data_1.wav`
(the source acoustic recording). Final PDFs in `figures/`.

### `chapter5_qmerge/`

| Notebook | Purpose |
|---|---|
| `01_qmerge_engine.ipynb` | The compute engine: per-segment SSO row sweeps, direct full-state encoding baselines, brickwall preconditioning, and the Stage-2 reweighting success-probability sweeps. This is what writes `SSO results/` and `results/`. Hours of CPU time. |
| `02_haar_scaling_sweep.ipynb` | Reweighting success probability *P* vs *M* and *N* for Haar-random segments → `sweep_success_prob_*.csv` |
| `03_hardware_circuit_build.ipynb` | Builds the 53-qubit Stage-1 circuit (4 preparation registers × 10 qubits, 10-qubit storage, 2 index qubits, 1 ancilla) and exports the `.qpy` artefacts. Despite the `TAG`, this is the 4 × 1024 run. |
| `04_figures.ipynb` | **Produces Figures 3.1, 3.2, 5.3–5.7 and Table 5.1** |

Supporting modules, imported directly by the notebooks:

| Module | Role |
|---|---|
| `mre_prep.py` | Q-MERGE Stage 1: SELECT-SWAP compression circuits (Qiskit) |
| `sso_prep.py` | The SSO / MPS staircase state-preparation stack |
| `sso_rowprep.py` | Wraps `sso_prep` into Qiskit staircase row-prep circuits |
| `sso_framework_setup.py` | Earlier standalone copy of the SSO framework (used by `02_` and by `supplementary/`) |

Data, all in `chapter5_qmerge/`:

| Path | Contents |
|---|---|
| `R75 Ultrasound data.xlsx` | The 32 × 1024 ultrasound dataset (upsampled to 128 × 1024 in the M=32 analysis) |
| `SSO results/row_sweep_*/` | Per-segment SSO fidelities vs staircase depth (`row_fids.json`, `row_states.npz`, `sigma.npy`) |
| `SSO results/fullstate_*/` | Direct whole-state encoding baselines (`checkpoint.npz`) |
| `results/v_R75x4_M32_incr.pkl` | 5000 simulated Stage-1 measurement outcomes, baseline and preconditioned (Figure 5.5) |
| `sweep_success_prob_*.csv` | Haar-random scaling sweeps (Figure 5.7) |
| `shadow_branch_hw_4x1024_L1_mid.pkl` | Branch-resolved H2-1 shots, 450 per branch (150 each of X, Y, Z) |
| `shadow_vs_fidelity_rows_4x1024_L1_mid_vs_ideal.npz` | Noiseless ω-vs-fidelity calibration curve, 9000 points per branch |
| `mre_{qc,prep_circuits,target_data}_4x1024_L1_mid.*` | The submitted circuits and their target segments |
| `*_4x256_L1_mid.*`, `shadow_branch_hw.pkl`, `mre_qc.qpy`, … | The earlier 4 × 256 and 4 × 32 runs |

### `supplementary/`

Exploratory work that informed the thesis but produced no figure in it: an SU(4)
staircase alternative to Stage-2 reweighting, an IPR-reduction ansatz comparison,
the original 4 × 32 hardware build, row-by-row encoding experiments, and a
schematic diagram script.

---

## Figure provenance

| Thesis figure | Notebook (cell) | Principal inputs |
|---|---|---|
| 3.1 — MPS and TTN structures | `chapter5_qmerge/04_figures.ipynb` (13) | none (schematic) |
| 3.2 — direct encoding fails on 32 × 1024 | `chapter5_qmerge/04_figures.ipynb` (18) | `SSO results/fullstate_R75x4_M32/checkpoint.npz` |
| 4.1 — SSO staircase + τ reducing layer | `chapter4_certification/05_figures.ipynb` (8) | none (schematic) |
| 4.2 — acoustic signal before/after basis change | `chapter4_certification/05_figures.ipynb` (5, 6) | KZB gate list, inlined in cell 1 |
| 4.3 — shadow overlap vs fidelity | `chapter4_certification/05_figures.ipynb` (18) | `shadows_vs_fidelity.npy` |
| 4.4 — shadow overlap histograms | `chapter4_certification/05_figures.ipynb` (13) | `shadow_results_{hardware,emulator}.pkl`, `shadow_results_noiseless.npy` |
| 4.5 — τ vs IPR, before and after | `chapter4_certification/05_figures.ipynb` (22) | `tau_ipr_{before,after}.npy` |
| 5.3 — the ultrasound dataset | `chapter5_qmerge/04_figures.ipynb` (17) | `R75 Ultrasound data.xlsx` |
| 5.4 — infidelity vs CNOT depth and CPU time | `chapter5_qmerge/04_figures.ipynb` (20) | `SSO results/row_sweep_*`, `fullstate_R75x4_M32` |
| 5.5 — reweighting success probability | `chapter5_qmerge/04_figures.ipynb` (16) | `results/v_R75x4_M32_incr.pkl` |
| 5.6 + Table 5.1 — per-branch H2-1 results | `chapter5_qmerge/04_figures.ipynb` (10) | `shadow_branch_hw_4x1024_L1_mid.pkl`, calibration `.npz` |
| 5.7 — *P* vs *M* for Haar-random segments | `chapter5_qmerge/04_figures.ipynb` (12) | `sweep_success_prob_vs_M.csv` |

Figures 5.1 and 5.2 (the Q-MERGE circuit diagrams) are drawn in LaTeX in the thesis
source and have no code here.

## Reproducing the headline numbers

| Result | Where |
|---|---|
| Q-MERGE infidelity 3.5 × 10⁻⁹ vs 6.2 × 10⁻³ direct | `chapter5_qmerge/04_figures.ipynb`, cell 20 |
| Preconditioning raises *P* from 0.0098 to 0.3170 | `chapter5_qmerge/04_figures.ipynb`, cell 16 |
| Weighted branch fidelity 0.7135 ± 0.0720 on H2-1 | `chapter5_qmerge/04_figures.ipynb`, cell 10 |
| τ reduced 447.29 → 17.49 for the acoustic target | `chapter4_certification/02_tau_reducing_layer.ipynb` |
| *F*_SSO = 0.9959, *F*_hw ≈ 0.91 | `chapter4_certification/05_figures.ipynb` |

## Notes

- **Quantinuum submission code is not included.** The notebooks that submitted jobs
  to H2-1 required account credentials and are omitted. Everything they produced is
  committed as raw data, so all analysis and plotting reproduces without machine
  access.
- Notebooks are committed **with their outputs** so the results are readable on
  GitHub without running anything.
- Paths are resolved relative to the working directory. A few comments still mention
  the original `C:\qruns\...` scratch location; those checkpoints now live under
  `chapter5_qmerge/SSO results/`.
- Re-running a figure cell writes its PDF **next to the notebook**, not into
  `figures/`. The `figures/` directories hold the versions used in the thesis, so
  regenerating never silently overwrites them.

## Related publications

1. A. Butterworth, J. Green, Y. Wu, J. Pan, J. Wang, *Efficient quantum state
   preparation on Quantinuum hardware*, arXiv [quant-ph] (2026).
2. A. Butterworth, J. Renders, J. Wang, *Q-MERGE: Parallelising quantum state
   preparation for large-scale classical data*, arXiv [quant-ph] (2026).

## Acknowledgements

Quantinuum provided access to the H2-1 trapped-ion quantum computer, and the Pawsey
Supercomputing Research Centre provided compute time on Setonix. The SSO method is
due to Green, Snow and Wang; `mps-to-circuit` is used under its own licence.
