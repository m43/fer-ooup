#include <iostream>
#include <cassert>
#include <cstdlib>

struct Point {
    int x = 100;
    int y = 1000;
};
struct Shape {
    enum EType {
        circle, square, rhombus
    };
    EType type_;
};
struct Circle {
    Shape::EType type_;
    double radius_;
    Point center_;
};
struct Square {
    Shape::EType type_;
    double side_;
    Point center_;
};
struct Rhombus {
    Shape::EType type_;
    Point center_;
    double side_;
    double angle_;
};

void drawSquare(struct Square *) {
    std::cerr << "in drawSquare\n";
}

void drawCircle(struct Circle *) {
    std::cerr << "in drawCircle\n";
}

void drawRhombus(struct Rhombus *) {
    std::cerr << "in drawRhombus\n";
}

void drawShapes(Shape **shapes, int n) {
    for (int i = 0; i < n; ++i) {
        struct Shape *s = shapes[i];
        switch (s->type_) {
            case Shape::square:
                drawSquare((struct Square *) s);
                break;
            case Shape::circle:
                drawCircle((struct Circle *) s);
                break;
            case Shape::rhombus:
                drawRhombus((struct Rhombus *) s);
                break;
            default:
                assert(0);
                exit(0);
        }
    }
}

void moveSquare(struct Square *s, int dx, int dy) {
    s->center_.x += dx;
    s->center_.y += dy;
    std::cerr << "Square moved by dx=" << dx << " and dy=%d" << dy << "\n";
}

void moveCircle(struct Circle *c, int dx, int dy) {
    c->center_.x += dx;
    c->center_.y += dy;
    std::cerr << "Circle moved by dx=" << dx << " and dy=%d" << dy << "\n";
}

void moveRhombus(struct Rhombus *r, int dx, int dy) {
    r->center_.x += dx;
    r->center_.y += dy;
    std::cerr << "Rhombus moved by dx=" << dx << " and dy=%d" << dy << " lalala\n";
}

void moveShapes(Shape **shapes, int n, int dx, int dy) {
    for (int i = 0; i < n; i++) {
        struct Shape *s = shapes[i];
        switch (s->type_) {
            case Shape::EType::square:
                moveSquare((struct Square *) s, dx, dy);
                break;
            case Shape::EType::circle:
                moveCircle((struct Circle *) s, dx, dy);
                break;
                // NOTE: uncommenting the next three lines will make the program work!
//            case Shape::rhombus:
//                moveRhombus((struct Rhombus *) s, dx, dy);
//                break;
            default:
                assert(0);
                exit(0);
        }
    }
}

int main() {
    Shape *shapes[4];
    shapes[0] = (Shape *) new Circle;
    shapes[0]->type_ = Shape::circle;
    shapes[1] = (Shape *) new Square;
    shapes[1]->type_ = Shape::square;
    shapes[2] = (Shape *) new Square;
    shapes[2]->type_ = Shape::square;
    shapes[3] = (Shape *) new Circle;
    shapes[3]->type_ = Shape::circle;
    shapes[4] = (Shape *) new Rhombus;
    shapes[4]->type_ = Shape::rhombus;

    drawShapes(shapes, 5);
    moveShapes(shapes, 5, 30, 120);
    return 0;
}
