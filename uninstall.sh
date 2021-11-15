printf "This has not been implemented yet"

exit


### UNINSTALL ###

if [[ "$OSTYPE" == "darwin"* ]]
then
  printf "Running MacOS\n"
  launchctl unload "$HOME/Library/LaunchAgents/com.samsterckval.watchgoat.plist"
  printf "Unloaded launchd service @ %s\n" "$HOME/Library/LaunchAgents/com.samsterckval.watchgoat.plist"
  sudo rm "$HOME/Library/LaunchAgents/com.samsterckval.watchgoat.plist"
  printf "Removed launchd file\nAll done, bye.\n(PS, the watchgoat executable still exists @ ~/bin/watchgoat)\n"
  exit 0
elif [[ "$OSTYPE" == "linux"* ]]
then
  printf "Running Linux\n"
  sudo systemctl disable watchgoat.timer
  sudo systemctl stop watchgoat.timer
  printf "Stopped the systemd service\n"
  sudo rm "/etc/systemd/system/watchgoat.service"
  sudo rm "/etc/systemd/system/watchgoat.timer"
  printf "Removed the systemd files, bye.\n(PS, the watchgoat executable still exists @ ~/bin/watchgoat)\n"
  exit 0
fi