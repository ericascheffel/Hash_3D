void setup() { 
 //Initialize serial and wait for port to open:
  Serial.begin(9600); 
  
  // prints title with ending line break 
  // Serial.println("ASCII Table ~ Character Map"); 
} 

// the loop routine runs over and over again forever:
void loop() {
  Serial.println("Nova Leitura");
  Serial.println(" 0 0 0 0 0 0 0 0 0");
  Serial.println(" 0 0 0 0 0 0 0 0 0");
  Serial.println(" 0 0 0 0 0 0 0 0 0");
  delay(500);               // wait for a second
}
