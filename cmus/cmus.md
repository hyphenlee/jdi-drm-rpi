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
  
