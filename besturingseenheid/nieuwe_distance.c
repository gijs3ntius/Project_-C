

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#define F_CPU 16E6			     // 16.0 Mhz clock

#define HIGH 0x1
#define LOW 0x0
#define IN 0
#define OUT 1

// Delay between measures (on msec) , may occur problem if delay is short.Check datasheet

volatile char is_measuring = 0;
volatile uint8_t Timer0_counter = 0 ;
volatile uint8_t distance;

volatile long echo_start = 0;
volatile long echo_duration = 0;


#define trigPin 2
#define echoPin 4


/* Ultrasenoorsensor
*********************************************************************************************************************/

void setUpUltra(){
	digital_config(trigPin, OUT); // trigger pin wordt output
	digital_config(echoPin, IN); // echo pin is input
}

void setUpInterrupt(){
	PORTD |= (1<<echoPin);		// Enable PD2 pull-up resistor. // digital_write(echoPin, 1)
	
	EIMSK  |= (1<<INT1);			// Enable INT1 interrupts.
	
	EICRA |= (1<<ISC11);		// The rising edge of INT1 generates an interrupt request.
	// dit betekent: als er iets binnenkomt op de echopin wordt er een interrupt gegeven.
}

void setUpTimer0(){
	
    TCCR1A = 0;
	TCCR0B |= (1<<CS00);						   // NO prescaller , every tick is 1us  - START
	TCNT0 = 0;								   // Clear counter
	TIMSK0 |= (1<<TOIE0);					   // Enable Timer0-Overflow interrupts
	sei();										// Global interrupts Enabled.
}

void startPulse(){
	digital_write(trigPin, LOW); // zorg ervoor dat trigger leeg is!
	_delay_us(2);
	
	digital_write(trigPin, HIGH);
	
	_delay_us(10);
	digital_write(trigPin, LOW);
	
}


uint8_t calcDistance(){
	uint8_t dis;
	echo_duration = Timer0_counter; // keer 256 omdat hij pas 1 optelt na 256 ticks
	_delay_ms(1);
	dis = (echo_duration * 0.034 / 2); // het moet wel passen, vandaar bitshift
	return dis;
	
}


/* dit is een soort van de main functie. Hierdoor krijg je de juiste afstand terug. Dit in scheduler gooien */
	
uint8_t getDistance(){
	
		if (is_measuring == 0)
		{
			is_measuring = 1;
			startPulse();
			_delay_ms(10);
			distance = calcDistance();
			transmitSerial(5);
	
		}

		return distance;	
}
	
	

ISR(TIMER0_OVF_vect)  // Here every time Timer0 Overflow
{
	if (digital_read(echoPin) == LOW)
	{
		echo_start = 0;
		transmitSerial(4); // hier gaat het mis dus dit morgen uitzoeken!!!!!!!!!!
		// ook kijken of het misgaat bij het veranderen naar een 8bits getal.
	}
	
	if (echo_start)
	{
		Timer0_counter += 1; // hij telt tot 255 dan geeft hij een overflow. Bij overflow tellen we er 1 bij op
		transmitSerial(3);
	}
	
	
} 


ISR(INT1_vect)
{
	
	if (echo_start == 0)
	{
		TCNT0 = 0; // clear counter
		Timer0_counter = 0; // clear de timer counter
		echo_start = 1;
		transmitSerial(2);
	}
}

