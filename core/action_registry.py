from features import absoluteduplicate, absolutepaste, pluginmenu

# Centralized action registry
action_registry = {
    "hk_absolutepaste": absolutepaste.run,
    "hk_absoluteduplicate": absoluteduplicate.run,
    "hk_effecttest": pluginmenu.run
}
