# Cura PostProcessingPlugin
# Author:   Simone Celestino
# Date:     January 21, 2019

# Description:  This plugin print insert in the gcode the current layer and the totale layer
#               M117 - displays the filename and layer height to the LCD

from ..Script import Script
from UM.Application import Application
import re

class DisplayCurrentLayerAndLayerCountOnLCD(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Display Current Layer And Layer Count On LCD",
            "key": "DisplayCurrentLayerAndLayerCountOnLCD",
            "metadata": {},
            "version": 2,
            "settings":
            { }
        }"""
    
    def execute(self, data):
        if self.getSettingValueByKey("name") != "":
            name = self.getSettingValueByKey("name")
        else:
            name = Application.getInstance().getPrintInformation().jobName       
        lcd_text = "M117 " #display on the LCD
        i = 1
        totalLayers = 0
        for layer in data:
            display_text = lcd_text + str(i)
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                if line.startswith(';'):
                    if line.startswith(';LAYER_COUNT:'):
                        match = re.search(r"\d+.*",line) #get the total layer number in the layer count row
                        totalLayers = match.group(0)
                if line.startswith(";LAYER:"):
                    line_index = lines.index(line)
                    display_text = display_text + "/" + totalLayers; #display the current layer/total layers
                    lines.insert(line_index + 1, display_text)
                    i += 1
            final_lines = "\n".join(lines)
            data[layer_index] = final_lines
            
        return data
