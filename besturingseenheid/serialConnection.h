/*
 * library.h
 *
 * Created: 27-10-2017 15:02:14
 *  Author: Gijs
 */ 
/*
int isValidID(int number);
int connect(int ID*, int number);
int getConnected(int ID*);
int getData();
int sentData();
int readSensor();
int command();
*/

void transmitSerial(uint8_t data);
uint8_t receiveSerial();

void serialReactor();