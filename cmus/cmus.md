# CMUS setup for Colorberry with orangepi zero 2w
## feature:
* support typec earphone inline control button:volume up,volume down, play/pause,double click next track, triple click previous track
# setup
* copy [control.py](control.py) to ~/sbin/
* get device path by `evtest`,and modify control.py to set the correct device path.
* run: `crontab -e ` and append:
  ```shell
  @reboot /usr/bin/python3 /home/hyphen/sbin/control.py > /home/hyphen/cron_debug.log 2>&1
  ```
 * open /usr/share/kbd/keymaps/beepy-kbd.map
  ```shell
  keycode 184 = eight
  #volume down will input "Q", don't know why just disable it
  keycode 114 = F100 
  ```
 * edit keyboard driver to enable pause/plan button:
   src/input_modifiers.c
map_phys_alt_keycode():
keycode += 119; // See map file for result keys
//append after this line
```c++
if(keycode==164)keycode=184;
```

  
