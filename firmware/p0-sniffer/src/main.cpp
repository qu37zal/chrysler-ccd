#include <Arduino.h>

// P0 scaffold only. RX pin and transceiver are deliberately unassigned until
// the isolated receiver circuit and its voltage levels are validated.
static constexpr bool kTransmitEnabled = false;
static constexpr size_t kCaptureCapacity = 128;

void setup() {
  Serial.begin(921600);
  const uint32_t start = millis();
  while (!Serial && millis() - start < 1500) {}
  Serial.println("{\"type\":\"device\",\"project\":\"chrysler-ccd\",\"firmware\":\"0.1.0-scaffold\",\"mode\":\"receive-only\",\"tx_enabled\":false,\"rx_configured\":false}");
}
void loop() {
  // No GPIO is connected to a vehicle interface in this scaffold.
  delay(1000);
}
