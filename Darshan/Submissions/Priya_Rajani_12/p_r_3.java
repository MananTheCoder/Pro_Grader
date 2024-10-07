import java.util.Scanner;

public class p_r_3 {
    public static long factorial(int num) {
        if (num < 0) {
            return -1; // Factorial for negative numbers doesn't exist
        }
        if (num == 0 || num == 1) {
            return 1;
        }

        long fact = 1;
        for (int i = 2; i <= num; i++) {
            fact *= i;
        }
        return fact;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int num = scanner.nextInt();
        
        long result = factorial(num);
        System.out.println(result);
        
        scanner.close();
    }
}
