"""Generate the preliminary P0 ESP32-S3 carrier PCB with KiCad's pcbnew Python API."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "p0_carrier.kicad_pcb"
DSN_PATH = ROOT / "p0_carrier.dsn"
SES_PATH = ROOT / "p0_carrier.ses"
FP_ROOT = Path(sys.executable).resolve().parents[1] / "share" / "kicad" / "footprints"


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def vec(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def add_footprint(board, library: str, name: str, ref: str, value: str,
                  x: float, y: float, rotation: float = 0):
    fp = pcbnew.FootprintLoad(str(FP_ROOT / f"{library}.pretty"), name)
    if fp is None:
        raise RuntimeError(f"Cannot load footprint {library}:{name}")
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(vec(x, y))
    fp.SetOrientationDegrees(rotation)
    board.Add(fp)
    return fp


def add_net(board, name: str):
    net = pcbnew.NETINFO_ITEM(board, name)
    board.Add(net)
    return net


def connect(fp, pad_no: str, net):
    for pad in fp.Pads():
        if pad.GetNumber() == str(pad_no):
            pad.SetNet(net)
            return
    raise RuntimeError(f"Pad {pad_no} missing on {fp.GetReference()}")


def add_edge(board, a, b):
    shape = pcbnew.PCB_SHAPE(board)
    shape.SetShape(pcbnew.SHAPE_T_SEGMENT)
    shape.SetStart(vec(*a))
    shape.SetEnd(vec(*b))
    shape.SetLayer(pcbnew.Edge_Cuts)
    shape.SetWidth(mm(0.05))
    board.Add(shape)


def add_text(board, text: str, x: float, y: float, size: float = 1.0,
             layer=pcbnew.F_SilkS, angle: float = 0):
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(vec(x, y))
    item.SetTextSize(vec(size, size))
    item.SetTextThickness(mm(0.15))
    item.SetLayer(layer)
    item.SetTextAngle(pcbnew.EDA_ANGLE(angle, pcbnew.DEGREES_T))
    board.Add(item)


def build_board():
    board = pcbnew.BOARD()
    design = board.GetDesignSettings()
    design.SetCopperLayerCount(2)
    # FreeRouting may neck down at pad escapes; these signal-only nets allow 0.15 mm.
    design.m_TrackMinWidth = mm(0.15)
    default_class = pcbnew.NETCLASS("Default")
    default_class.SetTrackWidth(mm(0.20))
    default_class.SetClearance(mm(0.20))
    default_class.SetViaDiameter(mm(0.60))
    default_class.SetViaDrill(mm(0.30))
    design.m_NetSettings.SetDefaultNetclass(default_class)
    design.m_NetSettings.SetNetclass("Default", default_class)
    board.SetFileName(str(BOARD_PATH))

    # Board outline includes a preliminary USB opening at the DevKitC end.
    outline = [
        (0, 0), (88, 0), (88, 13), (82, 13), (82, 25),
        (88, 25), (88, 38), (0, 38), (0, 0),
    ]
    for start, end in zip(outline, outline[1:]):
        add_edge(board, start, end)

    nets = {name: add_net(board, name) for name in [
        "CCD_P_RAW", "CCD_N_RAW", "LOGIC_GND", "3V3", "RX_LOGIC",
        "DLC_SIGNAL_GND", "DLC_CHASSIS_GND",
    ]}

    # Internal OBD pigtail interface; pad numbers match J1962 pin numbers.
    j1 = add_footprint(board, "Connector_PinHeader_2.54mm",
                       "PinHeader_2x08_P2.54mm_Vertical", "J1", "OBD_PIGTAIL_1-16",
                       10.0, 16.5, 0)
    connect(j1, "3", nets["CCD_P_RAW"])
    connect(j1, "11", nets["CCD_N_RAW"])
    connect(j1, "5", nets["DLC_SIGNAL_GND"])
    connect(j1, "4", nets["DLC_CHASSIS_GND"])

    # Receiver is a separate, yet-to-be-designed protected mezzanine.
    j2 = add_footprint(board, "Connector_PinHeader_2.54mm",
                       "PinHeader_1x06_P2.54mm_Vertical", "J2", "RX_MEZZANINE_TBD",
                       20.0, 12.65, 0)
    for pad_no, net_name in [("1", "CCD_P_RAW"), ("2", "CCD_N_RAW"),
                             ("3", "LOGIC_GND"), ("4", "3V3"),
                             ("5", "RX_LOGIC")]:
        connect(j2, pad_no, nets[net_name])

    # ESP32-S3-DevKitC-1 v1.1 header sockets. The DevKit USB-C end faces +X.
    h1 = add_footprint(board, "Connector_PinSocket_2.54mm",
                       "PinSocket_1x22_P2.54mm_Vertical", "J3", "DEVKIT_J1",
                       26.0, 6.3, 90)
    h2 = add_footprint(board, "Connector_PinSocket_2.54mm",
                       "PinSocket_1x22_P2.54mm_Vertical", "J4", "DEVKIT_J3",
                       26.0, 31.7, 90)
    connect(h1, "1", nets["3V3"])
    connect(h1, "4", nets["RX_LOGIC"])  # Espressif J1-4 = GPIO4
    connect(h1, "22", nets["LOGIC_GND"])
    connect(h2, "1", nets["LOGIC_GND"])

    # Normally-open solder-link footprint keeps pin-5 signal ground separate.
    jp1 = add_footprint(board, "Jumper",
                        "SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm",
                        "JP1", "DLC_SIG_GND_LINK_DNP", 19.0, 34.0, 90)
    connect(jp1, "1", nets["DLC_SIGNAL_GND"])
    connect(jp1, "2", nets["LOGIC_GND"])

    # Mechanical guidance only; final dimensions depend on the selected pigtail,
    # exact DevKit revision, USB plug shell, and service access.
    add_text(board, "PIGTAIL", 4.5, 3.2, 0.8)
    add_text(board, "RAW CCD RX MEZZANINE", 19.0, 3.2, 0.8)
    add_text(board, "ESP32-S3 DEVKITC-1 v1.1", 40.0, 36.0, 0.8)
    add_text(board, "DRAFT - NOT FOR VEHICLE", 38.0, 20.0,
             0.8, layer=pcbnew.F_SilkS)

    pcbnew.SaveBoard(str(BOARD_PATH), board)
    if not pcbnew.ExportSpecctraDSN(board, str(DSN_PATH)):
        raise RuntimeError(f"KiCad DSN export failed: {DSN_PATH}")
    print(f"Saved {BOARD_PATH}")
    print(f"Exported {DSN_PATH}")
    for ref, fp in [("J3", h1), ("J4", h2)]:
        print(ref, {pad.GetNumber(): (pcbnew.ToMM(pad.GetPosition().x),
                                      pcbnew.ToMM(pad.GetPosition().y))
                    for pad in fp.Pads() if pad.GetNumber() in {"1", "4", "22"}})


def import_session():
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    if board is None:
        raise RuntimeError(f"Cannot load {BOARD_PATH}")
    if not SES_PATH.exists():
        raise RuntimeError(f"FreeRouting session not found: {SES_PATH}")
    if not pcbnew.ImportSpecctraSES(board, str(SES_PATH)):
        raise RuntimeError("KiCad SES import failed")
    # FreeRouting 2.5.0 may use a short 0.15 mm neckdown despite the 0.20 mm
    # netclass width. The carrier allows only signal-level current, so widen
    # those segments to the nominal 0.20 mm before saving and running DRC.
    widened = 0
    for track in board.GetTracks():
        if (type(track).__name__ == "PCB_TRACK"
                and pcbnew.ToMM(track.GetWidth()) < 0.20):
            track.SetWidth(mm(0.20))
            widened += 1
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Imported {SES_PATH} into {BOARD_PATH}; widened {widened} signal segments to 0.20 mm")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--import-ses", action="store_true")
    args = parser.parse_args()
    if args.import_ses:
        import_session()
    else:
        build_board()
