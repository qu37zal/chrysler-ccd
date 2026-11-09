# Local vendor model cache

Vendor models are **not redistributed in Git**. Their original notices and
licenses remain with downloaded files. Install LTspice and obtain these models
from the manufacturer links below; preserve the originals. These links were
checked on 2026-11-09. Availability can change.

| Local file | Manufacturer source | Model coverage |
|---|---|---|
| `LT1716.lib` | Installed LTspice 26.1.1 `lib.zip`, `lib/sub/LT1716.sub`; [product](https://www.analog.com/en/products/lt1716.html) | Encrypted LTspice-only family model. Does not establish H-grade or automotive #W qualification. |
| `2N7002Q.lib` | [Diodes model](https://www.diodes.com/spice/download/4577/2N7002Q.spice.txt) | Subcircuit D/G/S order; package physical pins differ. |
| `BSS84Q.lib` | [Diodes model](https://www.diodes.com/spice/download/4685/BSS84Q.spice.txt) | Subcircuit D/G/S order. |
| `MMBT3906.lib` | [Diodes model](https://www.diodes.com/spice/download/2962/MMBT3906.spice.txt) | PNP model `DI_MMBT3906`. |
| `BAV21W.lib` | [Diodes model](https://www.diodes.com/spice/download/1527/BAV21W.spice.txt) | Download named BAV21W declares `DI_BAV21WS` and contains `VCJO`; vendor naming/parameter inconsistency. |
| `BAV21W-ngspice.lib` | Local compatibility derivative of the preceding file | Only change: `VCJO=` to `CJO=`. Preserve the original. Used by both simulators. Confirm capacitance/leakage against purchased diode. |
| `LM5164-Q1_TRANS.LIB` | [TI unencrypted model ZIP](https://www.ti.com/lit/zip/snvmbp2) | PSpice model. Regulated in LTspice; failed the same fixture in ngspice. Thermal shutdown and quiescent current are explicitly not modeled. |
| `TLV76701_TRANS.lib` | [TI unencrypted model ZIP](https://www.ti.com/lit/zip/slvmcy1) | Adjustable TLV76701 family model; nominal transient load response, not thermal qualification. |
| `tlv1701.lib` | [TI TLV1701 models](https://www.ti.com/product/TLV1701#design-tools-simulation) | Earlier comparison fixture only. Superseded as the leading receiver candidate. |

The SHA-256 inventory in `../model-hashes.json` identifies the actual local files
used for recorded results. The Diodes model text was recovered from manufacturer
web responses after direct download access was refused. Byte hashes describe
that cached text, not an assertion that manufacturer transport formatting is fixed.

No model of MCU firmware, Wi-Fi, USB enumeration, arbitration, automotive pulses,
ESD destruction, connector wear, or production variation is provided. Passive
models and bounded loads are appropriate where semiconductor behavioral models
do not apply. Do not describe these limits as simulated when they were not exercised.
