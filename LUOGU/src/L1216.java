import java.util.Scanner;

public class L1216 {
    public static void main(String[] args) {
        /*
         * 思路：
         * 状态为：结束点为ｉ行ｊ列时最大的数字和
         * 状态转移方程：ｆ[i,j]=max(f[i-1,j-1],f[i-1,j])+a[i,j]
         * */
        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
        int[][] f=new int[n+1][n+1];
        int res=0;
        for(int i=1;i<=n;i++){

            for(int j=1;j<=i;j++){
                f[i][j]=scanner.nextInt();
                f[i][j]=(f[i-1][j]<f[i-1][j-1]?f[i-1][j-1]:f[i-1][j])+f[i][j];

            }

        }
        for(int i=1;i<=n;i++){
            res=res>f[n][i]?res:f[n][i];
        }

        System.out.println(res);
    }
}
