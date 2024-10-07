#include <iostream>
// should pass all
using namespace std;

int main()
{
    int n;
    cin >> n;
    if (n & 1)
    {
        cout << "NO";
    }
    else
    {
        cout << "YES";
    }
    return 1;
}