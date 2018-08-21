import java.util.Scanner;

public class DP1474 {
    /*
    * DP
    * */
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int v=scanner.nextInt();
        int n=scanner.nextInt();
        int[] vnum=new int[v+1];
        for(int i=1;i<=v;i++){
            vnum[i]=scanner.nextInt();
        }
        long[] dp=new long[n+1];
        dp[0]=1;
        for(int i=1;i<=v;i++ ){
            for(int j=vnum[i];j<=n;j++){
                dp[j]+=dp[j-vnum[i]];
            }
        }
        System.out.println(dp[n]);
    }
}
