# Ableton Upgrades
Ableton Upgrades is a spiritual successor to Live Enhancement Suite (LES), rewritten in Python for Ableton 12. While many of the features are the same, it is written completely fresh from scratch in Python.

## Features 
### Plugin Menu
The plugin menu is a customizable dropdown menu that allows you to quickly access and add plugins to tracks. You can set your own plugins in the menu_config.json file. You can also create submenus or folders within the dropdown, as well as dividers for further visual seperation. 

#### Usage
You can access it by double right clicking (unless you rebind it), and you can navigate around it with a mouse, and click to add a plugin.

(Add GIF of using menu)

#### Config
To add or change the config menu, you must edit the **menu_config.json** located at **config/menu_config.json**. This json document will then be loaded into the plugin menu. If you are familliar with how Live Enhancement Suite (LES) implements its config, then this will very simmilar. The main difference is that it must be formatted as a json document. 

To begin, either copy and paste the template, or create an empty bracket. 


##### Plugins
```
  {
    "label": "Utility",
    "command": "\"Utility.adv\""
  }
```
The label is the name that will be displayed in your menu. Command is the term that will be used to search for the plugin. If the plugin you want is not the first result, you can try putting the command in quotes. (Make sure to use escape characters where necessary as this is json. Here is a [link](https://www.google.com "Escape Characters") if you need help) If that still does not work, you can create a preset of the plugin and name it more specific. If you create a preset, you should also be able to add the file extention "**.adv**" to your search term to further narrow it down. Each item must be seperated by a comma.

##### Submenus
```
  {
    "label": "Synths",
    "submenu": [
      {
        "label": "Serum",
        "command": "\"Serum\" vst3"
      }
    ]
  }
```
Again, the label is the name that will be displayed on the menu. Instead of a command however, you add a submenu. The submenu should contain an array of items (An array can be created by placing items inside of brackets). You can also create nested submenus by placing this same structure inside. 


##### Dividers
```
  { "type": "divider" },
```
You can add a divider by writing this anywhere that items can go. 

##### Template
```
[
  {
    "label": "Instruments",
    "submenu": [
      {
        "label": "Keyscape",
        "command": "\"Keyscape\" vst3"
      },
      {
        "label": "Instrument Rack",
        "command": "\"Instrument Rack\""
      },
      { "type": "divider" },
      {
        "label": "Synths",
        "submenu": [
          {
            "label": "Serum",
            "command": "\"Serum\" vst3"
          }
        ]
      }
    ]
  },
  { "type": "divider" },
  {
    "label": "MIDI",
    "submenu": [
      {
        "label": "MIDI Pitch",
        "command": "MIDI Pitch"
      },
      {
        "label": "MIDI Monitor",
        "command": "MIDI Monitor"
      },
      { "type": "divider" },
      {
        "label": "Arpeggiator",
        "command": "Arpeggiator"
      }
    ]
  },
  { "type": "divider" },
  {
    "label": "Utility",
    "command": "\"Utility.adv\""
  },
  {
    "label": "Audio Effect Rack",
    "command": "Audio Effect Rack"
  }
```


