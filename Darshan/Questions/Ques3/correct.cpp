#include <iostream>
using namespace std;
//should pass all
long long factorial(int num) {
    if (num < 0)
        return -1; // Factorial for negative numbers doesn't exist
    if (num == 0 || num == 1)
        return 1;

    long long fact = 1;
    for (int i = 2; i <= num; i++) {
        fact *= i;
    }
    return fact;
}

int main() {
    int num;
    cin >> num;
    long long result = factorial(num);
    cout <<result;

    return 0;
}
