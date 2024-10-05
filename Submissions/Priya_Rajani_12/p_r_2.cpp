#include <iostream>
using namespace std;
// should pass none
bool isPrime(int num) {
    if (num <= 1)
        return false;
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0)
            return false;
    }
    return true;
}

int main() {
    int num;
    cin >> num;

    if (isPrime(num)) cout <<"NO";
    else cout <<"YES";

    return 0;
}

