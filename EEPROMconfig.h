/*
* Deze include file zorgt ervoor dat er waarden naar de EEPROM geschreven kunnen worden.
*
*/


void setArduinoID(uint8_t userinput);
uint8_t getArduinoID();

void setMaxRoll(uint8_t userInput);
uint8_t getMaxRoll();

void setMinRoll(uint8_t userInput);
uint8_t getMinRoll();

void setMaxTemp(uint8_t userInput);
uint8_t getMaxTemp();

void setMinTemp(uint8_t userInput);
uint8_t getMinTemp();

void setMaxLight(uint8_t userInput);
uint8_t getMaxLight();

void setMinLight(uint8_t userInput);
uint8_t getMinLight();

void setDefaultValues();




