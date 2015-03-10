#ifndef LEDProximity_h
#define LEDProximity_h

#include "Arduino.h"

class LEDProximity {
	public:
		LEDProximity(int led, int IRPin, int IRemitter, int proximity);
		int readIR(int);
		void controlLED();
		// void distanceread();
	private:
		int _led;
		int _IRPin;
		int _IRemitter;
		int _proximity;
		int _ambientIR;
		int _obstacleIR;
		int _value[];
		int _distance;
		int _times;
		int _readIR();
};

#endif