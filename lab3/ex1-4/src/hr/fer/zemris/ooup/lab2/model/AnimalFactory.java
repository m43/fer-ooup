package hr.fer.zemris.ooup.lab2.model;

import java.io.File;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;

public class AnimalFactory {

    static URLClassLoader urlClassLoader;

    public static Animal newInstance1(String animalKind, String name) {
        try {
            Class<Animal> clazz = null;
            clazz = (Class<Animal>) Class.forName("hr.fer.zemris.ooup.lab2.model.plugins." + animalKind);

            Constructor<?> ctr = clazz.getConstructor(String.class);
            Animal animal = (Animal) ctr.newInstance(name);

            return animal;

        } catch (Exception e) {
            // e.printStackTrace();
            return null;
        }
    }

    public static Animal newInstance2(String animalKind, String name) {
        try {

            if (urlClassLoader == null) {
                ClassLoader parent = AnimalFactory.class.getClassLoader();

                urlClassLoader = new URLClassLoader(new URL[] {
                        // Dodaj jedan direktorij (završava s /)
                        new File("/path/to/dir/").toURI().toURL(),
                        // Dodaj jedan konkretan JAR (ne završava s /)
                        new File("/path/to/jar.jar").toURI().toURL() }, parent);
            }

            Class<Animal> clazz = (Class<Animal>) urlClassLoader.loadClass("hr.fer.zemris.ooup.lab2.model.plugins." + animalKind);

            // ili
            // Class<Animal> clazz = (Class<Animal>) Class.forName("hr.fer.zemris.ooup.lab2.model.plugins." + animalKind, true, urlClassLoader);

            Constructor<?> ctr = clazz.getConstructor(String.class);
            Animal animal = (Animal) ctr.newInstance(name);

            return animal;

        } catch (Exception e) {
            // e.printStackTrace();
            return null;
        }
    }

}