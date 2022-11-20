void setup() {
  Serial.begin(9600);  // 시리얼 통신 초기화
  pinMode(S, INPUT);
}

void loop() {
  int val = analogRead(gas);
  Serial.print("Hall Fire ");
  Serial.print(analogRead(S), DEC);
  Serial.print(" Gas ");
  Serial.println(val);
  delay(100);
}