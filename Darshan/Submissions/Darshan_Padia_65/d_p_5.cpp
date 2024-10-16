#include <bits/stdc++.h>

using namespace std;
bool solve(){
    int n;
    cin>>n;
    int k;
    cin>>k;
    int flg=0; // ascending
    int z=0;
    int zz=0;
    for(int i = 1 ; i<n;i++){
        int p;
        cin>>p;
        if(z==0 and p>k){
            flg=0;
            zz=1;
        }
        if(zz==0 and p<k){
            flg= 1;
            z=1;

        }
        if(flg and p>k)return false;
        if(flg==0 and p<k)return false;
        k=p;
    }
    return true;
}
int main(){
    cout<<solve();
    return 0;
}
