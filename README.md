
## Andrew Paul - AM.EN.U4AIE20122.
## Hemanth Pusuluri - AM.EN.4AIE20157.

# Alchol_detection

This Arduino code is designed for an Alcohol Detection system. It appears to be a part of a project involving a sensor to detect alcohol levels, a LiquidCrystal display for output, LEDs, a buzzer, and a button for user input. Here's a breakdown of the code:

1. **Libraries and Definitions:**
   - The code includes the LiquidCrystal library for controlling LCDs.
   - Various constants are defined, such as pin numbers for the buzzer, LEDs, analog sensor, and a button.

2. **Global Variables:**
   - `limit`: Threshold value for alcohol detection.
   - `count`: Keeps track of the number of alcohol detections.
   - `timer`: Used for a countdown in emergency mode.
   - `emergency`: A boolean variable indicating whether the system is in emergency mode.

3. **Setup Function:**
   - Configures pin modes for the sensor, LEDs, buzzer, LCD, and button.
   - Initializes the LiquidCrystal object for the LCD.
   - Begins serial communication.

4. **Loop Function:**
   - Reads analog data from the alcohol sensor.
   - If emergency mode is activated, displays a message on the LCD and lights up an additional LED.
   - If alcohol level exceeds the limit, increments the count, activates the buzzer, and blinks an LED.
   - If alcohol level is below the limit, resets the count, timer, and turns off the buzzer and LEDs.
   - If the count reaches a certain threshold (40), it enters a countdown phase for emergency mode.
   - If the button is pressed during this countdown, emergency mode is activated.
   - If the count reaches 80, it displays a "Danger" message and locks the engine.

Note: The alcohol detection mechanism and emergency mode logic suggest that this code is likely part of a system aimed at preventing drunk driving, where emergency mode may be triggered if the alcohol levels are consistently high.
