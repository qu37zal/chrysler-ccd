#include "ccd_frame.h"

namespace ccd {
uint8_t checksum(const uint8_t* data, size_t size) {
  uint8_t sum = 0;
  for (size_t i = 0; i < size; ++i) sum = static_cast<uint8_t>(sum + data[i]);
  return static_cast<uint8_t>(~sum);
}
bool checksum_ok(const uint8_t* frame, size_t size) {
  return size >= 2 && checksum(frame, size - 1) == frame[size - 1];
}
} // namespace ccd
