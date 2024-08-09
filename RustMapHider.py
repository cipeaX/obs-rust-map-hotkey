import obspython as S
import time

class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_settings = obs_settings
        self.hotkey_id = S.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id
        self.load()

    def load(self):
        self.hotkey_saved_key = S.obs_data_get_array(self.obs_settings,  str(self._id))
        S.obs_data_array_release(self.hotkey_saved_key)
        self.hotkey_id = S.obs_hotkey_register_frontend(str(self._id), str(self._id), self.callback)
        S.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)
        self.save()

    def save(self):
        self.hotkey_saved_key = S.obs_hotkey_save(self.hotkey_id)
        S.obs_data_set_array(self.obs_settings, str(self._id), self.hotkey_saved_key)
        S.obs_data_array_release(self.hotkey_saved_key)

def mapkey_callback(pressed):

    if pressed:
        toggle(True)
    else:  
        time.sleep(data.delay)
        toggle(False)

def toggle(boolean):
    
    scene_names: list[str] = S.obs_frontend_get_scene_names()
    try:
        index1 = scene_names.index(data.scene1)
        index2 = scene_names.index(data.scene2)
    except ValueError:
        print("Couldnt find Scenes")
        return

    scene_list = S.obs_frontend_get_scenes()

    source1 = scene_list[index1]
    source2 = scene_list[index2]

    scene1 = S.obs_scene_from_source(source1)
    scene2 = S.obs_scene_from_source(source2)

    item1 = S.obs_scene_find_source(scene1, data.image1)
    item2 = S.obs_scene_find_source(scene2, data.image2)

    S.obs_sceneitem_set_visible(item1, boolean)
    S.obs_sceneitem_set_visible(item2, boolean)
    
    S.obs_source_release(source1)
    S.obs_source_release(source2)

def script_description():
    return "Original Script by knaxelbabyy \n\n+COOKED BY CIPEAX"

def script_properties():
    properties = S.obs_properties_create()
    S.obs_properties_add_text(properties, "rust_scene_name", "Main Scene Name", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(properties, "rust_vertical_scene_name", "Vertical Scene Name", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(properties, "rust_map_source_name", "Main Mapcover Image Name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(properties, "rust_map_vertical_source_name", "Vertical Mapcover Image Name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_float_slider(properties, "rust_map_delay", "Reveal Delay (.11 std) :", 0,1,.01)
    return properties

def script_update(settings):
    data.image1 = S.obs_data_get_string(settings, "rust_map_source_name")
    data.image2 = S.obs_data_get_string(settings, "rust_map_vertical_source_name")
    data.scene1 = S.obs_data_get_string(settings, "rust_scene_name")
    data.scene2 = S.obs_data_get_string(settings, "rust_vertical_scene_name")
    data.delay = S.obs_data_get_double(settings, "rust_map_delay")

def script_load(settings):
    data.hotkey = Hotkey(mapkey_callback, settings, "Rust Map Cover (Push to Hide)")
    data.image1 = S.obs_data_get_string(settings, "rust_map_source_name")
    data.image2 = S.obs_data_get_string(settings, "rust_map_vertical_source_name")
    data.scene1 = S.obs_data_get_string(settings, "rust_scene_name")
    data.scene2 = S.obs_data_get_string(settings, "rust_vertical_scene_name")
    data.delay = S.obs_data_get_double(settings, "rust_map_delay")

def script_save(settings):
    data.hotkey.save()

class Data:
    image1 = ""
    image2 = ""
    scene1 = ""
    scene2 = ""
    delay = 0.0
    hotkey = None 

data = Data()