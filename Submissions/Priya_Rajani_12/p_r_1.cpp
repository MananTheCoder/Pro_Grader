#include <iostream>
// should fail all
using namespace std;

int main(){
    int n;
    cin>>n;
    if(n&1){
        cout<<"YES";
    }else{
        cout<<"NO";
    }
    return 0;
}