import copy


def run_scenario(
    base_farm,
    actions,
    start_day,
    horizon_days
):
    """
    Run a what-if scenario starting from a cloned farm.

    base_farm   : FarmTwin (current state)
    actions     : dict {day: [action, ...]}
    start_day   : day to start scenario
    horizon_days: number of days to simulate
    """

    # Clone the farm (critical)
    farm = copy.deepcopy(base_farm)

    history = []
    history.append(farm.snapshot())

    for d in range(start_day, start_day + horizon_days):
        # Apply actions scheduled for this day
        if d in actions:
            for action in actions[d]:
                action.apply(farm)

        farm.advance_time(days=1)
        history.append(farm.snapshot())

    return history
