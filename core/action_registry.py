from features import absoluteduplicate, absolutepaste, betterredo, buplicate, pluginmenu

# Centralized action registry
action_registry = {
    "hk_absolutepaste": absolutepaste.run,
    "hk_absoluteduplicate": absoluteduplicate.run,
    "hk_betterredo": betterredo.run,
    "hk_buplicate": buplicate.run,
    "hk_pluginmenu": pluginmenu.run
}
