import struct
import argparse
from dataclasses import dataclass
from typing import BinaryIO


def bytesToInt(input: BinaryIO, numBytes: int) -> int:
    f = {1: "c", 2: "h", 4: "i", 8: "q"}[numBytes]
    return struct.unpack(f, input.read(numBytes))[0]


def bytesToFloat(input: BinaryIO, numBytes: int) -> float:
    f = {2: "e", 4: "f", 8: "d"}[numBytes]
    return struct.unpack(f, input.read(numBytes))[0]


@dataclass
class headerInfo(object):
    ID: int
    zCount: int
    yCount: int
    towerCount: int
    dtCount: int
    dz: float
    dy: float
    dt: float
    meanSpeed: float
    hubHeight: float
    bottomHeight: float
    slope: list[float]
    intercept: list[float]
    text: str


def readHeader(filePath: str, checkReadCount: bool = False) -> headerInfo:
    with open(filePath, "rb") as inFile:
        ID = bytesToInt(inFile, 2)
        zCount, yCount, towerCount, dtCount = [bytesToInt(inFile, 4) for n in range(4)]
        dz, dy, dt = [bytesToFloat(inFile, 4) for n in range(3)]
        meanSpeed, hubHeight, bottomHeight = [bytesToFloat(inFile, 4) for n in range(3)]
        slope = [0, 0, 0]
        intercept = [0, 0, 0]
        for n in range(len(slope)):
            slope[n] = bytesToFloat(inFile, 4)
            intercept[n] = bytesToFloat(inFile, 4)
        textCount = bytesToInt(inFile, 4)
        textBytes = inFile.read(textCount)
        text = textBytes.decode(encoding="ascii")
        byteCount = 70 + textCount
        if checkReadCount:
            print(f"Should have read {byteCount:d} bytes. File position reports {inFile.tell():d}")
        return headerInfo(
            ID,
            zCount,
            yCount,
            towerCount,
            dtCount,
            dz,
            dy,
            dt,
            meanSpeed,
            hubHeight,
            bottomHeight,
            slope,
            intercept,
            text,
        )


def report(header: headerInfo):
    print(header.text)
    print(f"file ID: {header.ID:d}")
    print(
        f"{header.zCount:d} grid points in z, {header.yCount:d} grid points in y,"
        f" {header.towerCount:d} tower points and {header.dtCount:d} points in each history."
    )
    print(f"{header.dz:f} z-spacing, {header.dy:f} y-spacing, {header.dt:f} time step.")
    print(
        f"{header.meanSpeed:f} mean speed, {header.hubHeight:f} hub height,"
        f" {header.bottomHeight:f} grid bottom height."
    )
    i, j, k = header.slope
    print(f"{i:f} {j:f} {k:f} slope.")
    i, j, k = header.intercept
    print(f"{i:f} {j:f} {k:f} intercept.")


def main(arguments: str):
    parser = argparse.ArgumentParser()
    parser.add_argument("filePath", help="File path of BTS file to read")
    args = parser.parse_args(arguments)
    header = readHeader(args.filePath)
    report(header)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
