# TrainStats Embedded probe

This project contains the software to make a hardware probe for _TrainStats_. This software was mainly created for _SBC_ cards like _Raspberry Pi_, _Orange Pi_, _Odroid_, _Nano Pi_ etc... but you can use it with your computer or any other platform with _Serial port_.

Soon, a web interface will be available to view your exports with an interactive map. It will be the subject of another repo.

_Disclamer:_ This project is not a [_people|vehicle|pet|what you want_] tracking system. This project is a train tracker for **analysis purposes** (speed in a section, average stop time). 


## Hardware prerequisties
 * Computer or SBC (we recommend the _Raspberry Pi Zero_ because is cheap and can consume **30mA** in IDLE!)
 * A GPS receiver (we have tested the _Ublox NEO-6 series_ and the _Ublox NEO-7 series_ but you can (normally) using any receiver respecting the _NMEA 0183_ standard)
 * External battery (needed if you want to power your SBC 😉)


## Software limitation
For the moment, the software only use _GPS_ and not use other positionning systems (_GLONASS, Baidu, Galileo_). We waiting to receive a _Ublox NEO-8M_ (or a contribution) to make the project compatible and trying to get more accurate data.


## Installation
You need to install different dependancies:
```bash
apt install -y git python3 python-pip
```

Now, clone this repo:
```bash
git clone https://github.com/themimitoof/trainstats-embedded trainstats
cd trainstats
```

Install _python dependancies_ with ```pip```:
```bash
pip install -r requirements.txt
```

Now to can start the probe on typing the command:
```bash
./trainstats.py -d /dev/ttyUSB0
```

_Note:_ replace ```/dev/ttyUSB0``` with the good serial port.

And voilà! The probe is collecting GPS data and write them into a file on the ```sessions``` folder's.

You can check all startup commands by typing:
```bash
./trainstats.py -h
```


## Tweaking the raspberry Pi
_This part available soon!_


## Contribution
You can contribute to this project on creating an issue or on making a merge request.