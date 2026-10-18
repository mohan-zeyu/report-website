I recently installed another Ubuntu system on my originally Windows ROG laptop.
1. You can install the `asusctl` tool to control the specific hardware with the ROG, like the keyboard light, light bar around your machine and charge limit as well.
	Interestingly, when the ubuntu has a little difference between ones I previously installed. I think it's because the computer of this brand does something.
2. When the lid switches off, it just suspended off, so i can't get access from ssh.
	To change this, go for `/etc/systemd/logind.conf` file, and you would find many setting choices.

	Here I want to talk about the `systemd` setting directory. 
	Normally, if we want to change the settings, we would like to do it in the Drop-in way, instead of directly changing the main configuration.
	1. create a folder adding `.d`, the `/etc/systemd/logind.conf.d`
	2. write files under `90-switch.conf`.
		Here you would ask why 90. 
		The settings will be loaded in alphabetical order. So .conf with bigger starting number will be loaded later, therefore they have a higher priority to overwrite earlier ones.
		Conventionally, the `10~50` is the system basic settings and `90~99` are defined by users so we can make sure the user defined settings will work.