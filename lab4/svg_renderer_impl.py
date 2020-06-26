from typing import List

from flat_colors import FlatUiColors
from point import Point
from renderer import Renderer


class SvgRendererImpl(Renderer):

    def __init__(self, filename, outline=FlatUiColors.WET_ASPHALT, fill=FlatUiColors.ALIZARIN):
        self.filename = filename
        self.lines = ['<svg xmlns="http://www.w3.org/2000/svg">']
        self.outline = outline
        self.fill = fill

    def save_and_close(self) -> None:
        self.lines.append("</svg>")
        with open(self.filename, "w") as f:
            f.writelines(self.lines)

    def draw_line(self, s: Point, e: Point):
        line = f'    <line x1="{s.x}" y1="{s.y}" x2="{e.x}" y2="{e.y}" stroke="{self.outline}" stroke-width="{4}" />'
        self.lines.append(line)

    def fill_polygon(self, points: List[Point]):
        line = '   <polygon points="{}" style="fill:{};stroke:{};stroke-width:{}" />'.format(
            ",".join([str(p.x) + "," + str(p.y) for p in points]), self.fill, self.outline, 1)
        self.lines.append(line)
