/*
 * CFile1.c
 *
 * Created: 10-10-2017 19:28:18
 *  Author: Gijs
 */ 

#include <avr/io.h>
#include <stdio.h>

#define TRUE 1
#define FALSE 0
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
 * Gets a value from a digital pin
 */
int digital_read(int pin) {
	if (pin < 8)
	{
		return (PINB & (1 << (pin%8)));
	} else {
		return (PINB & (1 << (pin%8)));
	}
}

/*
 * Configures an ADC pin
 */
void adc_config() {
	ADMUX |= _BV(REFS0); //Set reference voltage (see docs)
	ADCSRA |= _BV(ADPS2) | _BV(ADPS1) | _BV(ADPS0); // Set the prescaler
	ADCSRA |= _BV(ADEN); // Enable ADC
}

/*
 * Gets a value from an analog pin
 * https://gist.github.com/Wollw/2396604 code from Internet to read analog
 * TODO before reading setup the ADMUX and ADCSRA registers
 */
uint16_t adc_read(uint8_t adcx) {
	/* adcx is the analog pin we want to use.  ADMUX's first few bits are
	 * the binary representations of the numbers of the pins so we can
	 * just 'OR' the pin's number with ADMUX to select that pin.
	 * We first zero the four bits by setting ADMUX equal to its higher
	 * four bits. */
	ADMUX	&=	0xf0;
	ADMUX	|=	adcx;

	/* This starts the conversion. */
	ADCSRA |= _BV(ADSC);

	/* This is an idle loop that just wait around until the conversion
	 * is finished.  It constantly checks ADCSRA's ADSC bit, which we just
	 * set above, to see if it is still set.  This bit is automatically
	 * reset (zeroed) when the conversion is ready so if we do this in
	 * a loop the loop will just go until the conversion is ready. */
	while ( (ADCSRA & _BV(ADSC)) );

	/* Finally, we return the converted value to the calling function. */
	return ADC;
}
