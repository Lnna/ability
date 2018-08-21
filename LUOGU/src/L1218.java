import java.util.Scanner;

public class L1218 {

    private static int[] prime={2,3,5,7};
    private static int[] p2={1,3,7,9};
    private static int N=0;
    public static void main(String[] args) {

        System.out.println(isPrime(3333));
        Scanner scanner=new Scanner(System.in);
        N=scanner.nextInt();
        if(N==1){

            for(int i=0;i<prime.length;i++){
                System.out.println(prime[i]);
            }
        }else {
            for(int i=0;i<prime.length;i++){
                dfs(prime[i],2);
            }
        }
    }
    static void dfs(long a,int n){
        if(n>N) {
            System.out.println(a);
            return;
        }
        long tmp=a;
        for(int i=0;i<p2.length;i++){
            a=tmp*10+p2[i];
            if(isPrime(a)) dfs(a,n+1);
            a=tmp;
        }

    }
    static boolean isPrime(long a){
        for(int i=2;i<Math.sqrt(a)+1;i++){
            if(a%i==0) return false;
        }
        return true;
    }
}
