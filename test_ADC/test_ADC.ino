void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  analogReadResolution(12);
  //analogSetWidth(12);
  //analogSetCycles(1);
//  analogSetSamples(1);
 // analogSetClockDiv(1);
  //analogSetAttenuation(ADC_11db);
  adcStart(36);
}

void loop() {
  // put your main code here, to run repeatedly:

  Serial.print("0, 512, 1024, ");
  Serial.println(analogRead(36));

}
