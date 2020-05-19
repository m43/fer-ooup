package hr.fer.zemris.ooup.lab2.model.plugins;

import hr.fer.zemris.ooup.lab2.model.Animal;

public class Parrot extends Animal {

    private String animalName;

    public Parrot(String name) {
        animalName = name;
    }

    @Override public String name() {
        return animalName;
    }

    @Override public String greet() {
        return "Papiga!!";
    }

    @Override public String menu() {
        return "Zlivača";
    }
}