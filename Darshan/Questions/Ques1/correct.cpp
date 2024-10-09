#include <iostream>
// should pass all
using namespace std;

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        (n&1)?cout<<"NO\n":cout<<"YES\n";
    }
    return 0;
}