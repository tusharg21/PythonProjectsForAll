Link for making a script run at startup
-----------------------------------------
https://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html

Raspberry Pi - run program at start-up
------------------------------------------
Anyway, I wanted to get my Raspberry Pi to start no-ip dynamic dns service when it started-up, so I wouldn't have to remember to start it every time it was powered up.  For details on how to install no-ip on the Pi, see this post.

There are loads of ways of running a command at start-up in Linux but my favoured approach is to create an initialisation script in /etc/init.d and register it using update-rc.d.  This way the application is started and stopped automatically when the system boots / shutdowns.

Create script in /etc/init.d
sudo nano /etc/init.d/NameOfYourScript

Warning - its important you test your script first and make sure it doesn't need a user to provide a response, press "y" or similar, because you may find it hangs the raspberry pi on boot waiting for a user (who's not there) to do something!

Make script executable
sudo chmod 755 /etc/init.d/NameOfYourScript

Test starting the program
sudo /etc/init.d/NameOfYourScript start

Test stopping the program
sudo /etc/init.d/NameOfYourScript stop

Register script to be run at start-up
To register your script to be run at start-up and shutdown, run the following command:

sudo update-rc.d NameOfYourScript defaults

Note - The header at the start is to make the script LSB compliant and provides details about the start up script and you should only need to change the name.  If you want to know more about creating LSB scripts for managing services, see http://wiki.debian.org/LSBInitScripts

If you ever want to remove the script from start-up, run the following command:

sudo update-rc.d -f  NameOfYourScript remove

--------------
Actual Example
--------------

Path
----
/etc/init.d/MedicineReminder.sh

Contents of MedicineReminder.sh
-------------------------------
#!/bin/sh
sudo python /home/pi/myWorkspace/python_programs/MedicineReminder/MedicineReminder.py &

On command prompt in shell
--------------------------
sudo update-rc.d MedicineReminder.sh defaults
