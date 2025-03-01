from pynput import keyboard


class ModifierKeys:
    keys = {
        keyboard.Key.ctrl_l,
        keyboard.Key.shift_l,
        keyboard.Key.alt_l,
        keyboard.Key.cmd_l,
        keyboard.Key.ctrl_r,
        keyboard.Key.shift_r,
        keyboard.Key.alt_gr,
        keyboard.Key.cmd_r,
    }

    def __init__(self):
        self._pressed_keys = 0x00

    def press_key(self, key):
        if key == keyboard.Key.ctrl_l:
            self._pressed_keys ^= 0x01
        if key == keyboard.Key.shift_l:
            self._pressed_keys ^= 0x02
        if key == keyboard.Key.alt_l:
            self._pressed_keys ^= 0x04
        if key == keyboard.Key.cmd_l:
            self._pressed_keys ^= 0x08
        if key == keyboard.Key.ctrl_r:
            self._pressed_keys ^= 0x10
        if key == keyboard.Key.shift_r:
            self._pressed_keys ^= 0x20
        if key == keyboard.Key.alt_gr:
            self._pressed_keys ^= 0x40
        if key == keyboard.Key.cmd_r:
            self._pressed_keys ^= 0x80

    def release_key(self, key):
        self.press_key(key)

    def report(self):
        return self._pressed_keys
    


class NonModifierKeys:
    def __init__(self):
        self._pressed_keys = set()
        self._ctrl_shirt_keys = []

    def press_key(self, key):
        self._pressed_keys.add(self._normalize_key(key))

    def release_key(self, key):
        normalized = self._normalize_key(key)
        if normalized in self._pressed_keys:
            self._pressed_keys.remove(normalized)

    _character_map = {
        "0": 39,
        "!": 30,
        "@": 31,
        "#": 32,
        "$": 33,
        "%": 34,
        "^": 35,
        "&": 36,
        "*": 37,
        "(": 38,
        ")": 39,


        "-": 45,
        "_": 45,
        "=": 46,
        "+": 46,
        "[": 47,
        "{": 47,
        "]": 48,
        "}": 48,
        "\\": 49,
        "|": 49,
        ";": 51,
        ":": 51,
        "'":52,
        "\"": 52,

        "`":53,
        "~":53,

        ",":54,
        "<":54,
        ".":55,
        ">":55,
        "/":56,
        "?":56,
    }


    _non_letter_keys = {
        keyboard.Key.backspace: 42,
        keyboard.Key.caps_lock: 57,
        keyboard.Key.delete: 76,
        keyboard.Key.down: 81,
        keyboard.Key.end: 77,
        keyboard.Key.enter: 40,
        keyboard.Key.esc: 41,
        
        keyboard.Key.f1: 58,
        keyboard.Key.f2: 59,
        keyboard.Key.f3: 60,
        keyboard.Key.f4: 61,
        keyboard.Key.f5: 62,
        keyboard.Key.f6: 63,
        keyboard.Key.f7: 64,
        keyboard.Key.f8: 65,
        keyboard.Key.f9: 66,
        keyboard.Key.f10: 67,
        keyboard.Key.f11: 68,
        keyboard.Key.f12: 69,

        keyboard.Key.f13: 0,
        keyboard.Key.f14: 0,
        keyboard.Key.f15: 0,
        keyboard.Key.f16: 0,
        keyboard.Key.f17: 0,
        keyboard.Key.f18: 0,
        keyboard.Key.f19: 0,
        keyboard.Key.f20: 0,

        keyboard.Key.home: 74,
        keyboard.Key.left: 80,
        keyboard.Key.page_down: 78,
        keyboard.Key.page_up: 75,
        keyboard.Key.right: 79,

        keyboard.Key.space: 44,
        keyboard.Key.tab: 43,
        keyboard.Key.up: 82,
        keyboard.Key.media_play_pause: 0,
        keyboard.Key.media_volume_mute: 0,
        keyboard.Key.media_volume_down: 0,
        keyboard.Key.media_volume_up: 0,
        keyboard.Key.media_previous: 0,
        keyboard.Key.media_next: 0,
        keyboard.Key.insert: 73,
        keyboard.Key.menu: 0,
        keyboard.Key.num_lock: 0,
        keyboard.Key.pause: 0,
        keyboard.Key.print_screen: 70,
        keyboard.Key.scroll_lock: 0,
    }
    def _normalize_key(self, key):
        try:
            if 0x60 < ord(key.char) < 0x7B: # small letters
                return ord(key.char) - 93
            elif 0x40 < ord(key.char) < 0x5B: # capital letters
                return ord(key.char) - 61
            elif 0x00 < ord(key.char) < 0x1B: # ctrl+shift letters
                return ord(key.char) + 3
            elif 0x30 < ord(key.char) < 0x3A: # 1-9
                return ord(key.char) - 19
            else:
                return self._character_map.get(key.char, 0)
        except AttributeError as e:
            return self._non_letter_keys.get(key, 0)

    def report(self):
        r = list(self._pressed_keys)[:6] + [0]*(6-len(self._pressed_keys))
        # print(r)
        return f"{r[0]:02x} {r[1]:02x} {r[2]:02x} {r[3]:02x} {r[4]:02x} {r[5]:02x}"




modifier_keys = ModifierKeys()
non_modifier_keys = NonModifierKeys()

# The event listener will be running in this block
with keyboard.Events() as events:
    for event in events:
        if event.key == keyboard.Key.esc:
            break
        else:
            # print('Received event {}'.format(event))
            if event.key in ModifierKeys.keys:
                modifier_keys.press_key(event.key)
            else:
                if isinstance(event, keyboard.Events.Press):
                    non_modifier_keys.press_key(event.key)
                else:
                    non_modifier_keys.release_key(event.key)
            print(f'{modifier_keys._pressed_keys:02x} 00 {non_modifier_keys.report()}')



def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

