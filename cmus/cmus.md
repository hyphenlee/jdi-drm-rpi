# CMUS setup for Colorberry with orangepi zero 2w
## feature:
* support typec earphone inline control button
* volume up,volume down, play/pause
* double click next track, triple click previous track
* start/switch to cmus/cava tmux tab by single `c` command
# setup
* copy [control.py](control.py) to `~/sbin/`
* get device path by `evtest`,and modify control.py to set the correct device path.
* run: `crontab -e ` and append:
  ```shell
  @reboot /usr/bin/python3 /home/hyphen/sbin/control.py > /home/hyphen/cron_debug.log 2>&1
  ```
 * edit /usr/share/kbd/keymaps/beepy-kbd.map
  ```shell
  # remove keycode 164 == eight to enable play/pause
  keycode 184 = eight
  #volume down will input "Q", don't know why just disable it
  keycode 114 = F100 
  ```
 * edit keyboard driver to enable pause/plan button:
    src/input_modifiers.c  
    map_phys_alt_keycode():  
    `keycode += 119; // See map file for result keys`  
    //append after this line  
```c++
if(keycode==164)keycode=184;
```
* copy [cava-config](cava-config) as `~/.config/cava/config`, recommand to install cava from source with newer release.
* copy [start-cmus.sh](start-cmus.sh) to `~/sbin/` and add `alias c='~/sbin/start-cmus.sh'` in `.zshrc` so you can start/switch to cmus/cava panel by `c` command

