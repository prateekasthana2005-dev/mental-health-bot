import java.util.Scanner;
public class hjs {
   
    public static void main(String[] args) {
    //     System.out.println(884+3334);
    //     int x;
    //     x = 39;
    //     System.out.println(++x);
    //     Scanner sc=new Scanner(System.in);
    //     int num ;
    //     System.out.println("Enter number");
    //     num=sc.nextInt();
    //     System.out.println("square is "+(num * num));
    //     int y= 'A';
    //     System.out.println(y);
    //     int a,b,c;
    //     System.out.println("enter As age");
    //     a=sc.nextInt();
    //     System.out.println("enter Bs age");
    //     b=sc.nextInt();
    //     System.out.println("enter Cs age");
    //     c=sc.nextInt();
    //     if(a<b&&a<c){
    //         System.out.println("A sabse chota");

    //     }
    //     else if(b<a&&b<c){
    //         System.out.println("B sabse chota");

    //     }
    //     else if(c<b&&c<a){
    //         System.out.println("C sabse chota");

    //     }

 

    // }
    Scanner sc=new Scanner(System.in);
    for(int i=2;i<=100;i=i+2){
        System.out.println(i);
    }
    int n=sc.nextInt();
    int max=1;
    for(int i=1;i<n;i++){
        if(n%i==0){
            max=i;
        }
    }System.out.println(max);
}
}