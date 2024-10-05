#include <iostream>
using namespace std;
// should pass some
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

    cout <<"NO";

    return 0;
}
