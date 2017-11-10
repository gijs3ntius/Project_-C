/*
 * CFile1.c
 *
 * Created: 10-10-2017 19:28:18
 *  Author: Gijs
 */

#include <avr/io.h>
#include <stdio.h>

#define HIGH 1
#define LOW 0
#define IN 0
#define OUT 1

/*
 * Sets a digital pin to get input or output
 */
void digital_config(int pin, int value) {
	if(pin < 8) {
		if(value == 0) {
			DDRD = DDRD & ~(1 << pin);
		} else {
			DDRD = DDRD | (1 << pin);
		}

	} else {
		if(value == 0) {
			DDRB = DDRB & ~(1 << (pin%8));
		} else {
			DDRB = DDRB | (1 << (pin%8));
		}
	}
	return;
}

/*
 * Sets a digital pin to 0 or 1
 */
void digital_write(int pin, int value) {
	if(pin < 8) {
		if(value == 0) {
			PORTD = PORTD & ~(1 << pin);
		} else {
			PORTD = PORTD | (1 << pin);
		}

	} else {
		if(value == 0) {
			PORTB = PORTB & ~(1 << (pin%8));
		} else {
			PORTB = PORTB | (1 << (pin%8));
		}
	}
	return;
}

/*
 * Gets a value from a digital pin 1 or 0
 */
int digital_read(int pin) {
	if (pin < 8)
	{
		return (PIND & (1 << (pin%8)));
	} else {
		return (PINB & (1 << (pin%8)));
	}
}

/*
 * Configures an ADC pin in this case pin 0
 */
void analog_config() {
	ADMUX = 0x00; // reset ADC
	ADMUX |= (1<<REFS0); // sets reference voltage
	ADCSRA |= (1<<ADEN)|(1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2); // enable ADC, select ADC prescaler with ADPS
}

/*
 * Gets a value from an analog pin
 */
uint16_t analog_read(uint8_t adcx) {
	ADMUX = (ADMUX & 0x1B) | (adcx & 0x05); // mask the last three bits from admux
	ADCSRA |= (1<<ADSC); // analog read is started
	loop_until_bit_is_set(ADCSRA,ADSC);
	return (ADCH | ADCL); //return adc
}
