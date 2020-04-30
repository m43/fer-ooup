#include <iostream>
#include <cassert>
#include <cstdlib>
#include <vector>

using namespace std;

struct Point {
    int x = 100;
    int y = 1000;
};

class Shape {
public :
    virtual void draw() = 0;

    virtual void move(int dx, int dy) = 0;
};

class Square : public Shape {
    double side_;
    Point center_;

    virtual void draw() {
        cerr << "Sqare drawn." << endl;
    };

    virtual void move(int dx, int dy) {
        cerr << "Square moved by (" << dx << "," << dy << ")\n";
    }
};


class Circle : public Shape {
    // NOTE:    all derived classes are mocks and dont implement real functionality (i.e. the drawing functionality does
    //          not take into account any points or drawing, and the points like center_ are not used)
    Point center_;
    double radius;

    virtual void draw() {
        cerr << "Circle drawn." << endl;
    };

    virtual void move(int dx, int dy) {
        cerr << "Circle moved by (" << dx << "," << dy << ")\n";
    }
};

class Polyline : public Shape {
    vector<Point> points;

    virtual void draw() {
        cerr << "Polyline drawn." << endl;
    }

    virtual void move(int dx, int dy) {
        cerr << "Polyline moved by (" << dx << "," << dy << ")\n";
    }
};

class Rhombus : public Shape {
    Point center_;
    double side_;
    double angle_;

    virtual void draw() {
        cerr << "Rhombus drawn." << endl;
    }

    virtual void move(int dx, int dy) {
        cerr << "Rhombus moved by (" << dx << "," << dy << ")\n";
    }
};

void drawShapes(const std::vector<Shape *> &fig) {
    std::vector<Shape *>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++it) {
        (*it)->draw();
    }
}

void moveShapes(const std::vector<Shape *> &fig, int dx, int dy) {
    std::vector<Shape *>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++it) {
        (*it)->move(dx, dy);
    }
}

int main() {
    std::vector<Shape *> shapes;
    shapes.push_back(new Circle);
    shapes.push_back(new Square);
    shapes.push_back(new Square);
    shapes.push_back(new Circle());
    shapes.push_back(new Polyline());
    shapes.push_back(new Rhombus());

    drawShapes(shapes);
    moveShapes(shapes, 30, 120);
    return 0;
}

/*
 *  "Finally, implement the lecture solution, and comment on its properties."
 *  Using the OOP principles of C++ i is easy to avoid the problems faced in the first (procedural)
 *  solution to the same problem. It's easy to add new classes and polymorphic functionality, with
 *  no switch cases that are really hard to change because they cause an domino-effect when tried
 *  to change. Therefore, it is not rigid. This implementation is also not fragile, as one does not
 *  need to remember to update the switch statement when a new class is added. It does not require
 *  any changes in base function when a new derived class is implemented (open/closed principle).
 */