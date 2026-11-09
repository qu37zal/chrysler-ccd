#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>

namespace ccd {
// Wire format: address, length, data..., checksum. Checksum validation policy
// is implemented independently so unverified captures can still be retained.
struct Frame {
  uint64_t timestamp_us{};
  std::vector<uint8_t> bytes;
  bool checksum_present{};
  bool checksum_valid{};
  bool framing_error{};
};

// CCD checksum used by the community libraries: ones-complement sum of all
// preceding bytes. Kept isolated pending cross-check against OEM/protocol docs.
uint8_t checksum(const uint8_t* data, size_t size);
bool checksum_ok(const uint8_t* frame, size_t size);
} // namespace ccd
