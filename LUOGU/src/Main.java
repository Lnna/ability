



import org.omg.PortableServer.LIFESPAN_POLICY_ID;

import java.util.*;

public class Main {
    private static int res=0;
    private static int[][] graph;
    private static boolean[][] node;
    private static int[] cost;
    private static int n,m;
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n=sc.nextInt();
        m=sc.nextInt();
        graph=new int[n+1][n+1];
        node=new boolean[n+1][n+1];
        cost=new int[n+1];
        for(int i=0;i<m;i++){
            graph[sc.nextInt()][sc.nextInt()]=sc.nextInt();
        }
        int r=sc.nextInt();
        bfs(r);
        System.out.println(res);

    }
    private static void bfs(int r){
//        List<Map.Entry<Integer,Integer>> list=new ArrayList<>();
        Queue<Integer> queue=new ArrayDeque<>();
        queue.add(r);
        while (queue.size()>0){
            int x=queue.remove();
            for(int i=1;i<=n;i++){
                if(graph[x][i]==0 || node[x][i])
                    continue;
                queue.add(i);
                node[x][i]=true;
                res += graph[x][i];
            }
        }
    }

//    public static void main(String[] args) {
//        //4
//        System.out.println(Math.floorDiv(3,2));
//        Scanner sc = new Scanner(System.in);
//        int n = sc.nextInt();
//        int[] high=new int[n];
//        for(int i=0;i<n;i++){
//            high[i]=sc.nextInt();
//        }
//        int[] level=new int[n];
//        for(int i=0;i<n;i++){
//            int t=0;
//            for(int j=0;j<n;j++){
//                if(high[j]+1>high[i])
//                    continue;
//                else
//                    t+=Math.floorDiv(high[i],high[j]+1);
//            }
//            level[i]=t;
//        }
//        for(int i=0;i<n;i++)
//            if(i==n-1)
//                System.out.println(level[i]);
//            else
//                System.out.print(level[i]+" ");
//    }
}
