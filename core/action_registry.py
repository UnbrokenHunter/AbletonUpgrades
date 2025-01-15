from features import absoluteduplicate, absolutepaste, betterredo, pluginmenu

# Centralized action registry
action_registry = {
    "hk_absolutepaste": absolutepaste.run,
    "hk_absoluteduplicate": absoluteduplicate.run,
    "hk_betterredo": betterredo.run,
    "hk_pluginmenu": pluginmenu.run
}
