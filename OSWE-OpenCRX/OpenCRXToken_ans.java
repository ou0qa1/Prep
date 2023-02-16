import java.util.Random;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
 
public class OpenCRXToken {
 
    public static void main(String args[]) {
        try (BufferedReader br = new BufferedReader(new FileReader("time.txt"))) {
            int length = 40;

            String line = br.readLine();
            String[] values = line.split(",");

            long start = Long.parseLong(values[0]);
            long stop = Long.parseLong(values[1]);
            String token = "";

            for (long l = start; l < stop; l++) {
                token = getRandomBase62(length, l);
                System.out.println(token);
            }
        } catch (IOException e) {
            System.err.println("Error reading input file: " + e.getMessage());
            System.exit(1);
        }

    }
  
    public static String getRandomBase62(int length, long seed) {
        Random random = new Random(seed);
        String s = "";
        for (int i = 0; i < length; i++) {
            s = s + "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".charAt(random.nextInt(62));
        }
        return s;
    }
}
     
