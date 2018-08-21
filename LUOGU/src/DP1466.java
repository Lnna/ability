import java.util.Scanner;

public class DP1466 {
    private static int n=0;
    private static int s=0;
    private static int res=0;
    private static long[] dp;
    private static boolean[] flg;
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        n=scanner.nextInt();
        s=(1+n)*n/2;
        if(s%2==1){
            System.out.println(0);
        }else {
            dp=new long[s+1];
            dp[0]=1;
            for(int i=1;i<=n;i++){
                for(int j=s;j>=i;j--){
                    dp[j]=dp[j]+dp[j-i];
                }
            }
            System.out.println(dp[s/2]/2);
        }

    }
}
