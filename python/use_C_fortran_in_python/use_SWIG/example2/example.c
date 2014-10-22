 
 int fact(int n) {
     if (n <= 1) return 1;
     else return n*fact(n-1);
 }
 
 
 void main(int n){
    int result;
    result = fact(n);
    printf("%d\n",result);
 }