# Source inventory

Project: [qu37zal/chrysler-ccd](https://github.com/qu37zal/chrysler-ccd). Availability/relevance checked 2026-11-09. Recheck before reuse; record exact commit hash and license before deriving code.

| Source | URL | Relevance / status | License/hash |
|---|---|---|---|
| ChryslerScanner | https://github.com/laszlodaniel/ChryslerScanner | User-named repo; upstream URL may redirect/rename; audit needed | Pending |
| CCDBusTransceiver | https://github.com/laszlodaniel/CCDBusTransceiver | Hardware/transceiver implementation; inspect schematic before selection | Pending |
| CCDLibrary | https://github.com/laszlodaniel/CCDLibrary | Framing/checksum reference; no code copied | Pending |
| CCDPCIBusTransceiver | https://github.com/laszlodaniel/CCDPCIBusTransceiver | Dual physical-layer project; keep CCD/PCI separated | Pending |
| J1850VPWCore | https://github.com/laszlodaniel/J1850VPWCore | VPW is distinct from CCD; reference only | Pending |
| csouers/chrysler-ccd | https://github.com/csouers/chrysler-ccd | Community protocol reference; audit needed | Pending |
| CCD user manual | https://chryslerccdsci.files.wordpress.com/2020/05/880586-ccdbususersmanual.pdf | CCD interface/bus overview; OEM vehicle details still primary | Pending |
| Prowler 1999 information | https://workshop-manuals.com/plymouth/prowler/v6-3.5l_vin_g/ | 1999 Prowler service pages; CCD described as twisted pair, ~2.5V per conductor, divider network | Web mirror; cite relevant pages |
| OpenIC | https://github.com/OpenIC | Exact project/URL requires confirmation | Pending |
| Moddler CCD-Arduino-Mega | https://github.com/Moddler/CCD-Arduino-Mega | MIT, WIP/untested per README; lists CCD transceiver ICs and bias/termination jumpers | Commit pending |
| sigrok CCD decoder | https://github.com/majekw/sigrok-ccd-pd | Decoder covers subset, mostly Jeep ZJ '98; not Prowler validated | License/hash pending |
| Operation CHARM | https://www.operationcharm.com/ | Service literature access; model-year/manual access to verify | Pending |

Additional lead: Workshop Manuals service article says the 1999 Prowler CCD is a twisted pair, each line roughly 2.5 V, with a voltage divider network. Snap-on communications manual identifies Chrysler CCD at DLC pins 3 and 11; exact Prowler manual diagram must confirm. PCI uses DLC pin 2 and is not this interface.
