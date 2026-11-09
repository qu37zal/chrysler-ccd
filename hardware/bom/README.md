# Purchase exports

`ccd_frontend_bench_digikey.csv` and `ccd_frontend_bench_mouser.csv` contain the
same 14 grouped manufacturer-part-number lines for **one CCD bench front end**:
25 fitted components, including the transmit-power header but no shunt.
These are not the complete P0 assembly BOM or a fabrication release.

The source is `hardware/tools/build_ccd_frontend.py`, which also generates the
native schematic and per-component inventory. Quantities are exact per assembly,
with no hidden spare or board-count multiplier. Buy extra small discretes or use
bin stock after reviewing those quantities. Do not automatically substitute
similar-looking MOSFET, diode or comparator parts.

## Upload

- [DigiKey myLists](https://www.digikey.com/en/mylists): create/upload a list and
  map Manufacturer Part Number, Manufacturer, Quantity, Reference Designators.
  Review exact matches and select cut tape before adding matched lines to a cart.
- [Mouser FORTE](https://www.mouser.com/en/bomtool/): upload the CSV, map those
  columns, review matches, availability, packaging and order quantities, then
  transfer the selected matches to the cart. Its [Price & Availability
  Assistant](https://www.mouser.com/en/price-availability/) also accepts CSVs and
  manufacturer part numbers.

The files have no vendor SKU column: manufacturer orderables are authoritative,
and each distributor resolves its own cut-tape SKU. A CSV upload is not proof of
stock or a placed order. No account/cart changes or purchases were made.

## Supply observations and holds

Checked supplier pages on 2026-11-09. Stock figures are transient and may be
cached. DigiKey showed backorder for BSS84Q-7-F, BAV21W-7-F and MMBT3906-7-F.
Mouser search/product pages showed BSS84Q and BAV21W stock, but availability for
every line has **not** been verified through an uploaded BOM. BSS84Q stock was
particularly small. The CSV is a purchasing aid, not a promise of a single-vendor
complete order. Resolve those matches before treating this as an order-ready kit.

LT1716HS5#TRMPBF is the 125°C H-grade commercial orderable. Automotive #W grade
is a separate orderable and is not interchangeable as a qualification claim.
Its local SPICE model is a family model.

The complete board's order list will additionally need the protected power
network, ESP32 module/USB section, exact OBD plug, service/test parts and final
passives. The OBD connector and enclosure remain mechanically unresolved.
