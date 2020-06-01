# -*- coding: utf-8 -*-
from geometry.graphical_object import GraphicalObject
from model.document_model import DocumentModel
from point import Point
from states.idle_state import IdleState


class AddShapeState(IdleState):

    def __init__(self, prototype: GraphicalObject, document_model: DocumentModel):
        self.prototype = prototype
        self.dm = document_model

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        new_go = self.prototype.clone()
        new_go.translate(mouse_point)
        self.dm.add_graphical_object(new_go)
