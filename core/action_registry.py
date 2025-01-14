from features import absoluteduplicate, absolutepaste

# Centralized action registry
action_registry = {
    "hk_absolutepaste": absolutepaste.run,
    "hk_absoluteduplicate": absoluteduplicate.run,
}
