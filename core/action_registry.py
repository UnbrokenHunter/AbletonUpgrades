from features import automation1, automation2

# Centralized action registry
action_registry = {
    "do_action_a": automation1.run,
    "do_action_b": automation2.run,
}
