#ifndef PINIO_
#define PINIO_

#include <avr/io.h>
#include <stdio.h>

#define HIGH 1
#define LOW 0
#define IN 0
#define OUT 1

void digital_config(int pin, int value);
void digital_write(int pin, int value);
int digital_read(int pin);
void adc_config();
uint16_t adc_read(uint8_t adcx);


#endif PINIO_
