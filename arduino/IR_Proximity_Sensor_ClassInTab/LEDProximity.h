#ifndef LEDProximity_h
#define LEDProximity_h

#include "Arduino.h"

class LEDProximity {
        byte buffer[8];
	public:
		LEDProximity(int led, int IRPin, int IRemitter, int proximity);
                void setupProximity();
		void controlLED();
	private:
		int _led;
		int _IRPin;
		int _IRemitter;
		int _proximity;
		int _ambientIR;
		int _obstacleIR;
		int _value[];
		int _distance;
                int _readIR(int);
                void _distanceRead();
};

#endif
