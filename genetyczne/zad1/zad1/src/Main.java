import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.text.DecimalFormat;
import java.util.Random;


public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        //numbers();


        PrintStream out = new PrintStream(new FileOutputStream("output.txt"));
        System.setOut(out);

        String fname = "f10.dat";

        long s = -1;

        if (args.length == 2) {
            s = Integer.parseInt(args[0]);
            fname = args[1];
        }
        if (args.length == 1) {
            fname = args[0];
        }


        tiny_gp gp = new tiny_gp("datfiles/" + fname, -1);
        gp.evolve();


    }

    private static void numbers() {
        // f1x.dat ->  f(x) = 5*x^3 - 2x^2 + 3x - 17 dziedzina: [-10, 10], [0,100], [-1, 1], [-1000, 1000]
        // f2x.dat -> f(x) = sin(x) + cos(x) dziedzina: [-3.14, 3.14], [0,7], [0, 100], [-100, 100]
        // f3x.dat -> f(x) = 2* ln(x+1) dziedzina: [0,4], [0, 9], [0,99], [0,999]
        // f4x.dat -> f(x,y) = x + 2*y dziedzina: x i y [0, 1], [-10, 10], [0, 100], [-1000, 1000]
        // f5x.dat -> f(x, y) = sin(x/2) + 2* cos(x) dziedzina x, y: [-3.14, 3.14], [0,7], [0, 100], [-100, 100]
        // f6x.dat -> f(x,y) = x^2 + 3x*y - 7y + 1 dziedzina x,y: [-10, 10], [0,100], [-1, 1], [-1000, 1000]

        //Generowanie liczb do dat
        StringBuilder sb  = new StringBuilder();
        Random rand = new Random();
        for (double n = 0; n<100;n++){
            double x =(rand.nextDouble()* 2000)-1000;
            double y =(rand.nextDouble()* 2000)-1000;
            double z = x*x + 3*x*y - 7*y +1;
            DecimalFormat df = new DecimalFormat("#.##");
            sb.append(df.format(x)).append(" ").append(df.format(y)).append(" ").append(df.format(z)).append("\n");
        }
        sb = new StringBuilder(sb.toString().replaceAll(",", "."));
        System.out.println(sb);
    }

}