import java.util.Scanner;

public class p_r_2 {
    public static boolean isPrime(int num) {
        if (num <= 1) {
            return false;
        }
        for (int i = 2; i * i <= num; i++) {
            if (num % i == 0) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int num = scanner.nextInt();

        if (isPrime(num)) {
            System.out.println("NO");
        } else {
            System.out.println("YES");
        }
        
        scanner.close();
    }
}
