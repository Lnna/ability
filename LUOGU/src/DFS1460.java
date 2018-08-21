import java.util.Scanner;

public class DFS1460 {

    private static int v=0;
    private static int n=0;
    private static int[] vnum;
    private static int[][] nnum;
    private static int types;
    private static int[] pert,tmp;
    public static void main(String[] args) {
        /*
         * 题解：寻找解决方法的时候，如果遇到像这样对一个数组要来回遍历（不只是单纯的查找，包括这题的累加之类的
         * 总之是要重复很多次，记得优先想到用深度搜索的方法实现，搜索肯定能把所有情况考虑进去。
         *
         * 然而事实上，我并没有懂。。。
         * 它整个深搜是怎么走的。。。。。。好难好难好难
         * */
        Scanner scanner=new Scanner(System.in);
        v=scanner.nextInt();

        vnum=new int[v+1];

        for(int i=1;i<=v;i++){
            vnum[i]=scanner.nextInt();
        }

        n=scanner.nextInt();
        nnum=new int[n+1][v+1];

        for(int i=1;i<=n;i++){
            for (int j=1;j<=v;j++){
                nnum[i][j]=scanner.nextInt();
            }
        }
        types=n+1;
        pert=new int[n+1];
        tmp=new int[n+1];
        dfs(1,0);
        System.out.print(types+" ");
        for(int i=1;i<=types;i++){
            if(i==types)
                System.out.print(pert[i]);
            else
                System.out.print(pert[i]+" ");
        }

    }
    static boolean pd(int s){
        for(int i=1;i<=v;i++){
            int sum=0;
            for(int j=1;j<=s;j++){
                sum+=nnum[tmp[j]][i];
            }
            if(sum<vnum[i])
                return false;
        }
        return true;
    }
    static void dfs(int x,int s){
        if(x>n) {
            if(pd(s)){
                if(s<types){
                    types=s;
                    for(int i=1;i<=s;i++){
                        pert[i]=tmp[i];
                    }
                }

            }
            return;

        }
        tmp[s+1]=x;
        dfs(x+1,s+1);
        tmp[s+1]=0;
        dfs(x+1,s);

    }

}
