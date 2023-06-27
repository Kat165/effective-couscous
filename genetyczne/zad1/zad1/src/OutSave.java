import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

class OutSave
{

    static File output = new File("output.txt");

    public static void main() throws IOException {
        print("Print this");
        OutSave.print("And save this");
    }

    public static void print(String str) throws IOException {
    System.out.println(str);
    writeToFile(output, str);
}



    public static void writeToFile(File file, String str) throws IOException {
        BufferedWriter bw = new BufferedWriter(new FileWriter(file));
        bw.write(str);
        bw.close();
    }
}