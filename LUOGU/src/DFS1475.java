import java.util.Scanner;

public class DFS1475 {
    private static int[][] sum=new int[101][101];
    private static boolean[] own=new boolean[101];
    private static boolean[] flg=new boolean[101];
    private static int[] ct=new int[101];
    private static int m=0;
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
        for(int i=1;i<=n;i++){
            int a=scanner.nextInt();
            int b=scanner.nextInt();
            sum[a][b]=scanner.nextInt();
            m=Math.max(m,Math.max(a,b));
        }
        for(int i=1;i<=m;i++){
            for(int j=1;j<=m;j++){
                own[j]=false;
                ct[j]=0;
                flg[j]=false;
            }
            dfs(i);
            for(int j=1;j<=m;j++){
                if(own[j]&&i!=j){
                    System.out.println(i+" "+j);
                }
            }
        }

    }
    static void dfs(int x){
        if(flg[x]) return;
        flg[x]=true;
        for(int i=1;i<=m;i++){
            ct[i]+=sum[x][i];
            if(ct[i]>50){
                own[i]=true;
                dfs(i);
            }
        }
    }

}
