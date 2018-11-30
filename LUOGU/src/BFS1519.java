import java.util.*;

public class BFS1519 {
    /*
     * 算法设计：
     * 数据结构：二维数组存储迷宫，(2w,2h)表示方格坐标，{+1,-1}表示四面的坐标,{+2,-2}表示方格前进坐标。
     * 步骤：不需要找到迷宫的两个出口的坐标表示，遇到空字符即表示到了出口；
     * 从第一个方格开始，深度搜索到出口的最短路径；
     * 然后搜索第二个方格，选择两个最短路径中较大的路径长度，因为要保证任意一点都能在这个步数内出去；
     * 重复上述过程，直到搜索完全部方格，输出最小步数。
     * */
    private static int W=0;
    private static int H=0;
    //    方格坐标
    private static char[][] rooms;
    //    四面坐标
    private static int[] wx={0,-1,0,1};
    private static int[] wy={1,0,-1,0};


    //    flg标示每个坐标是否走过
    private static boolean[][] flg;

    //    出口坐标
    private static int x1=0,y1=0;
    private static int x2=0,y2=0;

    private static int[][] min_path;
    private static int max_min_path=0;
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        W=scanner.nextInt();
        H=scanner.nextInt();
        scanner.nextLine();
        String[] s=new String[2*H+2];
        for(int i=1;i<=2*H+1;i++){
            s[i]=scanner.nextLine();

        }
        min_path=new int[H+1][W+1];
//        System.out.println(System.currentTimeMillis());
        rooms=new char[2*H+2][2*W+2];
        flg=new boolean[2*H+2][2*W+2];
        for(int i=1;i<=2*H+1;i++){
            for(int j=1;j<=2*W+1;j++){
                flg[i][j]=false;
                if(s[i].length()==1 || s[i].length()<j){
                    rooms[i][j]=' ';
                }else
                    rooms[i][j]=s[i].charAt(j-1);
            }
        }
        for(int i=1;i<=2*H+1;i++){
            if(rooms[i][1]==' '){
                if(x1==0 && y1==0){
                    x1=i;
                    y1=2;
                }else {
                    x2=i;
                    y2=2;
                }
            }
            if(rooms[i][2*W+1]==' '){
                if(x1==0 && y1==0){
                    x1=i;
                    y1=2*W;
                }else {
                    x2=i;
                    y2=2*W;
                }
            }
        }
        for(int i=1;i<=2*W+1;i++){
            if(rooms[1][i]==' '){
                if(x1==0 && y1==0){
                    x1=2;
                    y1=i;
                }else {
                    x2=2;
                    y2=i;
                }
            }
            if(rooms[2*H+1][i]==' '){
                if(x1==0 && y1==0){
                    x1=2*H;
                    y1=i;
                }else {
                    x2=2*H;
                    y2=i;
                }
            }
        }
        for(int i=1;i<=H;i++){
            for(int j=1;j<=W;j++){
                min_path[i][j]=10000;
            }
        }
        bfs(x1,y1);
        for(int i=1;i<=2*H+1;i++){
            for(int j=1;j<=2*W+1;j++){
                flg[i][j]=false;

            }
        }
        bfs(x2,y2);

        for(int i=1;i<=H;i++){
            for(int j=1;j<=W;j++){
                if(max_min_path<min_path[i][j])
                    max_min_path=min_path[i][j];
            }
        }
        System.out.println(max_min_path);

    }
    private static void bfs(int x,int y){
        List<Map.Entry<Integer,Integer>> queue=new ArrayList<>();
        queue.add(new AbstractMap.SimpleEntry<>(x,y));
        int pos1=1,pos2=0;
        int path=1;
        min_path[x/2][y/2]=1;
        while (queue.size()>0){

            Map.Entry<Integer,Integer> pair=queue.remove(0);
            pos1--;

            int hx=pair.getKey();
            int hy=pair.getValue();
            for(int i=0;i<4;i++){
                if(hx+wx[i]>1 && hx+wx[i]<2*H+1 && hy+wy[i]>1 && hy+wy[i]<2*W+1
                        && rooms[hx+wx[i]][hy+wy[i]]==' ' && !flg[hx+wx[i]][hy+wy[i]]){
                    flg[hx+wx[i]][hy+wy[i]]=true;
                    pos2++;
                    queue.add(new AbstractMap.SimpleEntry<>(hx+2*wx[i],hy+2*wy[i]));
                    if(min_path[(hx+2*wx[i])/2][(hy+2*wy[i])/2]>path+1){
                        min_path[(hx+2*wx[i])/2][(hy+2*wy[i])/2]=path+1;
                    }

                }
            }
            if(pos1==0) {
                path++;
                pos1=pos2;
                pos2=0;
            }
        }
    }

}
