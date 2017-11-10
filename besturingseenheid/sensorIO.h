/* include file voor temperatuur sensor */

// Ultrasenoorsensor
//int getDistance();

// Photocell sensor
int getLight();

// Temperatuur sensor
int getTemp();


void rolledInOrOut(uint8_t command, uint8_t maxOut);

void resetLights();