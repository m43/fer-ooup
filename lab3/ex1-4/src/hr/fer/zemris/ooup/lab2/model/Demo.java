package hr.fer.zemris.ooup.lab2.model;

import java.util.Random;

public class Demo {

    static String names[] = { "X Æ A-11", "Alcabú", "Covarrubias", "Bautista", "Miguel", "Mancebo", "Piñón", "Nico", "Ramon", "Sancho" };

    public static void main(String[] args) {
        String[] animals = { "Tiger", "Parrot" };

        for (String animalName : animals) {
            int nameNumber = new Random().nextInt(names.length);

            Animal animal = AnimalFactory.newInstance1(animalName, names[nameNumber]);
            if (animal == null) {
                animal = AnimalFactory.newInstance2(animalName, names[nameNumber]);
                if (animal == null) {
                    System.out.println("Could not load '" + animalName + "'");
                    continue;
                }
            }

            animal.animalPrintGreeting();
            animal.animalPrintMenu();
        }
    }

}
