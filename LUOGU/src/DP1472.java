import java.util.Scanner;

public class DP1472 {
    /*
     * dp:考虑n个节点小于等于k层的情况数，而状态转移，将t个节点分给左子树，剩下的节点分给右子树
     * */
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
        int k=scanner.nextInt();
        int mod=9901;
        int[][] dp=new int[n+1][k+1];
        for(int i=1;i<=k;i++) dp[1][i]=1;
        for(int i=1;i<=k;i++){
            for(int j=3;j<=n;j+=2){
                for(int m=1;m<j;m+=2){
                    dp[j][i]=(dp[j][i]+dp[m][i-1]*dp[j-1-m][i-1])%mod;

                }
            }
        }
//        <=k的个数可能小于小于等于k-1的个数
        System.out.println(((dp[n][k]-dp[n][k-1]+mod)%mod));
    }
}
