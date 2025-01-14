from features import absoluteduplicate, absolutepaste, addplugin

# Centralized action registry
action_registry = {
    "hk_absolutepaste": absolutepaste.run,
    "hk_absoluteduplicate": absoluteduplicate.run,
    "hk_effecttest": addplugin.run
}
