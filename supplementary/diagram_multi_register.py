# =============================================================================
#  SCHEMATIC -- hub-and-spoke illustration of multi-register encoding
# =============================================================================
#
#  A presentation figure, not a thesis figure: M loading registers arranged around
#  a central storage+index register, with circular flow arrows and a protocol
#  flowchart sidebar. Written for talks and the poster.
#
#  The thesis circuit diagrams (Figs. 5.1 and 5.2) are drawn in LaTeX/quantikz in
#  the thesis source instead, and are not produced by this script.
#
#  Standalone -- needs only numpy and matplotlib. Run it directly.
#
# =============================================================================

"""
Multi-Register Quantum Encoding Diagram
========================================
Hub-and-spoke diagram: M loading registers around a central storage+index
register, with circular flow arrows and a protocol flowchart sidebar.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D

# ── Palette (white background) ────────────────────────────────────────────────
BG         = 'white'
CENTER_BG  = '#dce8f8'
CENTER_RIM = '#3d5ef5'
BLUE       = '#3d5ef5'    # storage qubits
GREEN      = '#16a34a'    # index qubits
ORANGE     = '#e05c20'    # loading-register atoms
LINE_COL   = '#16a34a'    # spoke dashes
FLOW_COL   = '#64748b'    # circular flow arrows
TEXT       = '#111827'
GREY       = '#64748b'
LOOP_COL   = '#e05c20'    # loop-back arrow in flowchart

DOT_R   = 0.115
SPACING = 0.295
RADIUS  = 3.85            # distance from centre to each loading register


# ── Helpers ───────────────────────────────────────────────────────────────────

def draw_qubit_grid(ax, cx, cy, rows, cols, colour, dot_r=DOT_R, spacing=SPACING):
    w = (cols - 1) * spacing
    h = (rows - 1) * spacing
    for r in range(rows):
        for c in range(cols):
            x = cx - w / 2 + c * spacing
            y = cy + h / 2 - r * spacing
            ax.add_patch(Circle((x, y), dot_r, color=colour, zorder=6, linewidth=0))


def curved_arrow(ax, p1, p2, rad=-0.38, color=FLOW_COL, lw=1.6, zorder=5):
    """Draw a curved arrow from p1 to p2, curving outward (rad < 0)."""
    ax.annotate(
        '', xy=p2, xytext=p1,
        arrowprops=dict(
            arrowstyle='->', color=color, lw=lw,
            connectionstyle=f'arc3,rad={rad}',
        ),
        zorder=zorder,
    )


def flowchart_box(ax, cx, cy, w, h, title_num, body_text,
                  fc='#f0f5ff', ec=BLUE):
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.12',
        facecolor=fc, edgecolor=ec, linewidth=1.6, zorder=3,
    )
    ax.add_patch(box)
    ax.text(cx - w / 2 + 0.18, cy, title_num,
            color=BLUE, fontsize=11, fontweight='bold',
            ha='left', va='center', zorder=4)
    ax.text(cx - w / 2 + 0.52, cy, body_text,
            color=TEXT, fontsize=8.8,
            ha='left', va='center', zorder=4)
    return cy  # return centre y for arrow placement


# ── Main function ─────────────────────────────────────────────────────────────

def make_diagram(save_path='multi_register_diagram.png'):

    fig = plt.figure(figsize=(17, 10), facecolor=BG)
    gs  = gridspec.GridSpec(1, 2, width_ratios=[2.2, 1], wspace=0.04)

    ax  = fig.add_subplot(gs[0])   # main hub diagram
    axf = fig.add_subplot(gs[1])   # flowchart panel

    for a in (ax, axf):
        a.set_facecolor(BG)
        a.axis('off')

    # ────────────────────────────────────────────────────────────────────────
    # MAIN DIAGRAM
    # ────────────────────────────────────────────────────────────────────────
    ax.set_xlim(-6.3, 6.3)
    ax.set_ylim(-6.3, 6.8)
    ax.set_aspect('equal')

    # Central glow + background
    for r, a in [(1.85, 0.10), (1.65, 0.18), (1.50, 0.30)]:
        ax.add_patch(Circle((0, 0), r, color=CENTER_RIM, alpha=a, zorder=1))
    ax.add_patch(Circle((0, 0), 1.42, color=CENTER_BG, zorder=2))
    ax.add_patch(Circle((0, 0), 1.44, color=CENTER_RIM, alpha=0.45,
                         fill=False, lw=1.5, zorder=2))

    # Storage qubits (blue) 3×4, index qubits (green) 1×3
    draw_qubit_grid(ax, 0,  0.38, 3, 4, BLUE)
    draw_qubit_grid(ax, 0, -0.52, 1, 3, GREEN)

    _lbox = dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.82, edgecolor='none')
    ax.text(0, -0.90, 'Storage + index', color=TEXT, fontsize=10.5,
            ha='center', va='center', fontweight='bold', zorder=7, bbox=_lbox)
    ax.text(0, -1.13, '(always coherent)', color=GREY, fontsize=8,
            ha='center', va='center', zorder=7, style='italic', bbox=_lbox)
    ax.text(0, -1.33, 'Never measured mid-protocol',
            color=GREY, fontsize=7, ha='center', va='center', zorder=7, bbox=_lbox)

    # Loading registers: (angle°, subscript, rows, cols, special)
    regs = [
        ( 90, '0', 2, 4, 'top'),
        (138, '1', 2, 4, None),
        (180, '2', 2, 4, None),
        (222, '3', 2, 4, None),
        (316, '4', 2, 4, 'measure'),
        (  2, '5', 2, 4, None),
        ( 48, '6', 2, 4, None),
    ]

    reg_positions = []   # (rx, ry) for each register in order

    for angle_deg, sub, nrows, ncols, special in regs:
        angle = np.radians(angle_deg)
        rx = RADIUS * np.cos(angle)
        ry = RADIUS * np.sin(angle)
        reg_positions.append((rx, ry))

        # Spoke (dashed green)
        t0, t1 = 1.46, 0.70
        ax.plot(
            [t0 * np.cos(angle), rx - t1 * np.cos(angle)],
            [t0 * np.sin(angle), ry - t1 * np.sin(angle)],
            color=LINE_COL, ls='--', lw=1.2, alpha=0.6, zorder=3,
        )

        # Loading register background
        ax.add_patch(Circle((rx, ry), 0.70, color='#f0f4fb', zorder=4))
        ax.add_patch(Circle((rx, ry), 0.72, color=CENTER_RIM, alpha=0.25,
                             fill=False, lw=1.2, zorder=4))

        # Orange dots
        draw_qubit_grid(ax, rx, ry, nrows, ncols, ORANGE)

        # Label
        push = 1.02
        lx = rx + push * np.cos(angle)
        ly = ry + push * np.sin(angle)
        ax.text(lx, ly, f'$A_{{{sub}}}$', color=TEXT, fontsize=13,
                ha='center', va='center', fontweight='bold', zorder=8)

        if special == 'top':
            ax.text(lx, ly + 0.48, '— loading register',
                    color=GREY, fontsize=8, ha='center', va='bottom', zorder=8)

        if special == 'measure':
            ax.annotate(
                'Measure +\nreload classical bay',
                xy=(rx + 0.62, ry - 0.18),
                xytext=(rx + 2.15, ry - 1.25),
                color=GREY, fontsize=8.5, ha='left', va='center', zorder=9,
                arrowprops=dict(arrowstyle='->', color='#3d5ef5', lw=1.5,
                                connectionstyle='arc3,rad=-0.22'),
            )

    # ── Circular flow arrows between consecutive registers ────────────────────
    # Order by angle (counterclockwise): 2°, 48°, 90°, 138°, 180°, 222°, 316°
    # We want a clean clockwise cycle arrow around the outside.
    # Use the regs list order (already sorted by angle going CCW from A_5 → A_6 → A_0 → …)
    # Draw arrow from each register to the next (counterclockwise = increasing angle).
    # rad > 0 curves left (away from centre when going CCW).

    order = [4, 5, 6, 0, 1, 2, 3]   # index into regs: A_4→A_5→A_6→A_0→A_1→A_2→A_3→A_4
    ARROW_R = 0.65   # offset from centre of register toward neighbour

    for k in range(len(order)):
        i = order[k]
        j = order[(k + 1) % len(order)]
        rx_i, ry_i = reg_positions[i]
        rx_j, ry_j = reg_positions[j]

        # Direction vectors: i→j
        dx = rx_j - rx_i
        dy = ry_j - ry_i
        dist = np.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist  # unit vector i→j

        # Start point: edge of register i toward j
        p1 = (rx_i + ARROW_R * ux, ry_i + ARROW_R * uy)
        # End point: edge of register j from i side
        p2 = (rx_j - ARROW_R * ux, ry_j - ARROW_R * uy)

        # Outward curvature: positive rad curves left (outward for CCW travel)
        curved_arrow(ax, p1, p2, rad=0.32, color=FLOW_COL, lw=1.5)

    # Circular "cycle" label
    ax.text(0, 5.75, 'Sequential loading cycle  →',
            color=FLOW_COL, fontsize=8.5, ha='center', va='center',
            style='italic', zorder=8)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_items = [
        Line2D([0], [0], marker='o', color='none', markerfacecolor=BLUE,
               markersize=11, label='Storage qubits'),
        Line2D([0], [0], marker='o', color='none', markerfacecolor=GREEN,
               markersize=11, label='Index qubits'),
        Line2D([0], [0], marker='o', color='none', markerfacecolor=ORANGE,
               markersize=11, label='Loading register atoms'),
        Line2D([0], [0], color=LINE_COL, ls='--', lw=1.8,
               label='Controlled-SWAP link'),
        Line2D([0], [0], color=FLOW_COL, ls='-', lw=1.8,
               marker='>', markersize=6, label='Loading cycle direction'),
    ]
    ax.legend(
        handles=legend_items,
        loc='lower center', bbox_to_anchor=(0.5, -0.02),
        ncol=3, fontsize=8.8,
        facecolor='#f8faff', edgecolor='#c0c8e8',
        labelcolor=TEXT, framealpha=0.95,
        handlelength=2.0, borderpad=0.9, labelspacing=0.5,
    )

    # ────────────────────────────────────────────────────────────────────────
    # FLOWCHART PANEL
    # ────────────────────────────────────────────────────────────────────────
    axf.set_xlim(0, 4.2)
    axf.set_ylim(-1.2, 10.5)
    axf.set_aspect('equal')

    # Title
    axf.text(2.1, 10.0, 'Protocol', color=TEXT, fontsize=13,
             fontweight='bold', ha='center', va='center')
    axf.text(2.1, 9.55, 'for each loading register $A_k$',
             color=GREY, fontsize=8.5, ha='center', va='center', style='italic')

    BW, BH = 3.5, 1.05
    cx_box = 2.1
    steps = [
        ('1.', 'Prepare quantum\nsubstate on  $A_k$'),
        ('2.', 'Controlled-SWAP:\npush  $A_k$  into storage'),
        ('3.', 'Measure  $A_k$\n(read classical outcome)'),
        ('4.', 'Increment  $k$,\nload next register'),
    ]

    box_tops = []
    box_bots = []
    gap = 0.55
    y0  = 8.8

    for i, (num, body) in enumerate(steps):
        cy = y0 - i * (BH + gap)
        box_tops.append(cy + BH / 2)
        box_bots.append(cy - BH / 2)

        fc = '#fff7f0' if i == 2 else '#f0f5ff'
        ec = LOOP_COL  if i == 2 else BLUE

        flowchart_box(axf, cx_box, cy, BW, BH, num, body, fc=fc, ec=ec)

        # Arrow down to next box
        if i < len(steps) - 1:
            axf.annotate(
                '', xy=(cx_box, cy - BH / 2 - gap + 0.05),
                xytext=(cx_box, cy - BH / 2),
                arrowprops=dict(arrowstyle='->', color=TEXT, lw=1.4),
                zorder=5,
            )

    # Loop-back arrow: step 4 bottom → step 1 top, on the left side
    y_start = box_bots[-1]
    y_end   = box_tops[0]
    x_left  = cx_box - BW / 2 - 0.45

    # Vertical left rail
    axf.plot([x_left, x_left], [y_start, y_end],
             color=LOOP_COL, lw=1.6, zorder=4)
    # Bottom connector
    axf.plot([cx_box - BW / 2, x_left], [y_start, y_start],
             color=LOOP_COL, lw=1.6, zorder=4)
    # Arrowhead into step 1
    axf.annotate(
        '', xy=(cx_box - BW / 2, y_end),
        xytext=(x_left, y_end),
        arrowprops=dict(arrowstyle='->', color=LOOP_COL, lw=1.6),
        zorder=5,
    )
    axf.text(x_left - 0.12, (y_start + y_end) / 2, '↺  repeat',
             color=LOOP_COL, fontsize=9, ha='right', va='center',
             fontweight='bold', rotation=90,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3ee',
                       edgecolor=LOOP_COL, alpha=0.9, linewidth=1.2))

    # Note about parallelism
    y_note = box_bots[-1] - 0.6
    axf.text(2.1, y_note,
             'While storage processes $A_k$,\nnext register prepares in parallel.',
             color=GREY, fontsize=8, ha='center', va='top',
             style='italic', wrap=True)

    # ── Save ──────────────────────────────────────────────────────────────────
    plt.savefig(save_path, dpi=200, bbox_inches='tight',
                facecolor=BG)
    print(f'Saved → {save_path}')
    plt.show()


make_diagram()
