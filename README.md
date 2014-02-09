pyAlienFX
=========

This project is a multiplatform python software to control the AlienFX device of Alienware computers.  It intend to be easily upgradable for future updates of the AlienFX device, as it happened for the M11XR3. And, to be a powerfull GTK apps, that can be linked with plugins throught a deamon server, allowing the LED to be controled accordingly !  Any Help is more than welcome ! Especially testing on different computers ! 

LAST VERSION

Stable Version 1.0
NEWS

    Arch Linux Support :
        Dear all, thanks to Alejandro we now have a working package for Arch Linux ! Instruction bellow ! 

    1.0.2 Stable
        Added support for M18XR2 

    1.0.1 Stable
        Corrected small bug affecting some users on M14XR2 due to Profiles from M11X which went in the package ! 

    1.0 Stable
        Modification of the GUI
        A lot of bug corrections
        Adding Deb Packaging to the project
        Better support of different models
        ENJOY ! 

    0.2 Beta
        Modification of the Installer Script
        Modification of the GUI 

    0.2.2 Alpha
        Correction of a Major bug affecting the M17X (And I supose others (see  Issue 2 ))
        Adding the support for the M14XR1 Thanks to LightHash? ! 

    0.2.1 Alpha
        Corrections of Minor bugs that improves stability of light changes ! 

    0.2 Alpha
        Install Script (install.py to be exectued with sudo)
        Indicator Applet (Ubuntu Unity only !)
        The driver is now controled by a daemon which is launched at startup!
        Bugs : For a reason that I do not understand, the Indicator Applet produce changes in the lights. 

    0.1.1 Beta
        Support for AlienWare? M17XR3 !
        Added Profile Manager, Saving/Loading Profiles !
        Improved Advance configurator, removing items from line !
        Added Lights ON/OFF (Menu Option) 

    V0.1 Beta released
        New GUI
        Save after reboot
        Advanced mode 

!!! WARNING !!!

    This is a Beta
    The code here has only been tested on the Alienware M11XR3 with the USB controler 0x187c:0x0522 BUT should work on any M11X
    Update : The M17XR3 is also tested an functional !
    Please if you can test it on one of the model listed here and send me your feedback it would be really helpful ! 

How To Install

How To : How to use :

    install libusb 1.0 : http://www.libusb.org/
    extract the pyAlienFX-v0.2a.tar.gz file to any folder
    enter the folder pyalienfx/
    execute : sudo ./install.py
    to launch the Configurator : launch pyAlienFX (Alt+F2 pyAlienFX, or in the Unity Dash or in a terminal)
    To have the Indicator please add the pyAlienFX_Launcher.sh to the list of Startup software (any help on how to automatize this would be welcome !) 

How to DEB :

    Double click on the deb file ! 

How to Arch Linux:

    Easy way (using yaourt package manager):
        yaourt -S pyalienfx 

    Using the Arch Build System:
        Download the PKGBUILD from: https://aur.archlinux.org/packages/pyalienfx/
        "makepkg -s" on PKGBUILD directory
        "sudo pacman -U {package}.tar.xz" 

Command How To :

    sudo apt-get update
    sudo apt-get install libusb-1.0
    cd
    cd Download
    tar zxvf pyAlienFX.tar.gz
    cd pyalienfx
    python ./pyAlienFX.py 

Credit :

Thanks to Wattos for his software AlienFX Lite, which helped me a lot understanding how to build the driver.

Thanks to PyUSB http://sourceforge.net/apps/trac/pyusb/

Thanks to LibUSB http://www.libusb.org/ 
