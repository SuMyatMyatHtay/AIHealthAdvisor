const int buzzerPin = 9;  // Buzzer connected to pin 9
const int buttonPin = 8;  // Button connected to pin 8
const int ledPin = 7;     // LED connected to pin 7
int buttonState = 0;

void setup() {
  pinMode(buzzerPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // Using internal pull-up resistor
  Serial.begin(9600);
}

void loop() {
  // Read the state of the button
  buttonState = digitalRead(buttonPin);

  // Send the button state to Node-RED via serial communication
  if (buttonState == LOW) {
    Serial.println("ON"); // Button pressed
  } else {
    Serial.println("OFF"); // Button not pressed
  }

  // Check for serial input from Node-RED
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any extra whitespace or newline characters

    if (command == "ON") {
      digitalWrite(buzzerPin, HIGH); // Turn on buzzer
      digitalWrite(ledPin, HIGH);    // Turn on LED
    } else if (command == "OFF") {
      digitalWrite(buzzerPin, LOW);  // Turn off buzzer
      digitalWrite(ledPin, LOW);     // Turn off LED
    }
  }
}