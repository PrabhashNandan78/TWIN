from Visualization.encoding import encode_plant_visual
from Visualization.plot2d import plot_farm


def plot_scenario_outcomes(
    history_a,
    history_b,
    label_a="Scenario A",
    label_b="Scenario B"
):
    """
    Compare final state of two scenarios visually.
    """

    final_a = history_a[-1]
    final_b = history_b[-1]

    encoded_a = [
        encode_plant_visual(p)
        for p in final_a["plants"]
    ]

    encoded_b = [
        encode_plant_visual(p)
        for p in final_b["plants"]
    ]

    plot_farm(
        encoded_a,
        title=f"Outcome: {label_a}"
    )

    plot_farm(
        encoded_b,
        title=f"Outcome: {label_b}"
    )
