from dataclasses import dataclass

import cv2
import numpy as np

import opsi.manager.cvwrapper as cvw
from opsi.manager.manager_schema import Function
from opsi.manager.types import Contours, Mat, MatBW, RangeType

OPENCV3 = False

if cv2.__version__[0] == "3":
    OPENCV3 = True

ERODE_DILATE_CONSTS = {
    "kernel": None,
    "anchor": (-1, -1),
    "borderType": cv2.BORDER_CONSTANT,
    "borderValue": -1,
}

FIND_CONTOURS_CONSTS = {"mode": cv2.RETR_LIST, "method": cv2.CHAIN_APPROX_SIMPLE}

__package__ = "demo.cv"
__version__ = "0.123"


class Blur(Function):
    @dataclass
    class Settings:
        radius: int

    @dataclass
    class Inputs:
        img: Mat

    @dataclass
    class Outputs:
        blurred: Mat

    def run(self, inputs):
        blurredImg = cvw.blur(inputs.img, self.settings.radius)
        return self.Outputs(blurred=blurredImg)


class HSVRange(Function):
    @dataclass
    class Settings:
        hue: RangeType(0, 255)
        sat: RangeType(0, 255)
        val: RangeType(0, 255)

    @dataclass
    class Inputs:
        img: Mat

    @dataclass
    class Outputs:
        masked: MatBW

    def run(self, inputs):
        lower = np.array(
            [
                self.settings.hue["min"],
                self.settings.sat["min"],
                self.settings.val["min"],
            ]
        )
        upper = np.array(
            [
                self.settings.hue["max"],
                self.settings.sat["max"],
                self.settings.val["max"],
            ]
        )
        masked = cv2.inRange(inputs.img, lower, upper)
        return self.Outputs(masked=masked)


class Erode(Function):
    @dataclass
    class Settings:
        size: int

    @dataclass
    class Inputs:
        img: MatBW

    @dataclass
    class Outputs:
        eroded: MatBW

    def run(self, inputs):
        eroded = cv2.erode(
            inputs.img, iterations=round(self.settings.size), **ERODE_DILATE_CONSTS
        )
        return self.Outputs(eroded=eroded)


class Dilate(Function):
    @dataclass
    class Settings:
        size: int

    @dataclass
    class Inputs:
        img: MatBW

    @dataclass
    class Outputs:
        dilated: MatBW

    def run(self, inputs):
        dilated = cv2.dilate(
            inputs.img, iterations=round(self.settings.size), **ERODE_DILATE_CONSTS
        )
        return self.Outputs(dilated=dilated)


class FindContours(Function):
    @dataclass
    class Settings:
        draw: bool

    @dataclass
    class Inputs:
        img: MatBW

    @dataclass
    class Outputs:
        contours: Contours
        visual: MatBW

    def run(self, inputs):
        if OPENCV3:
            vals = cv2.findContours(inputs.img, **FIND_CONTOURS_CONSTS)[1]
        else:
            vals = cv2.findContours(inputs.img, **FIND_CONTOURS_CONSTS)[0]
        if self.settings.draw:
            visual = cv2.drawContours(inputs.img, vals, -1, (255, 255, 255), 3)
            return self.Outputs(contours=vals, visual=visual)
        return self.Outputs(contours=vals, visual=inputs.img)


class FindCenter(Function):
    @dataclass
    class Settings:
        draw: bool

    @dataclass
    class Inputs:
        contours: Contours
        img: MatBW

    @dataclass
    class Outputs:
        center: int
        visual: Mat

    def run(self, inputs):
        image = cv2.cvtColor(inputs.img, cv2.COLOR_GRAY2BGR)
        midpoint = None
        for cnt in inputs.contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cx = (x + (x + w)) // 2
            cy = (y + (y + h)) // 2
            midpoint = (cx, cy)
            if self.settings.draw:
                image = cv2.circle(image, midpoint, 10, (0, 0, 255), 3)
        return self.Outputs(center=midpoint, visual=image)


class ConvexHulls(Function):
    @dataclass
    class Inputs:
        contours: Contours

    @dataclass
    class Outputs:
        contours: Contours

    def run(self, inputs):
        conts = [cv2.convexHull(contour) for contour in inputs.contours]
        return self.Outputs(contours=conts)


class MatBWToMat(Function):
    @dataclass
    class Inputs:
        bwMat: MatBW

    @dataclass
    class Outputs:
        regMat: Mat

    def run(self, inputs):
        return self.Outputs(regMat=cv2.cvtColor(inputs.bwMat, cv2.COLOR_GRAY2BGR))
