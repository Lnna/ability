import java.util.Scanner;

public class DFS1518 {
    private static char[][] roads=new char[11][11];
    private static int[] xd={-1,0,1,0};
    private static int[] yd={0,1,0,-1};
    private static boolean[][][][][][] flg=new boolean[11][11][4][11][11][4];
    private static int res=0;
    /*
     * 模拟暴力搜索
     * 注意：
     * xy坐标方向别搞错
     * 四个方向的表达方式：xd={-1,0,1,0}，yd={0,1,0,-1}
     * 判断条件：边界、障碍，方向改变；坐标方向一致走过，说明成环，不会再相遇
     * */
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int cx=0,cy=0;
        int fx=0,fy=0;
        for(int i=1;i<=10;i++){
            String s=scanner.next();
            for(int j=1;j<=10;j++){
                roads[i][j]=s.charAt(j-1);
                if(roads[i][j]=='C'){
                    cx=i;
                    cy=j;
                }
                if(roads[i][j]=='F'){
                    fx=i;
                    fy=j;
                }

            }
        }
        dfs(cx,cy,0,fx,fy,0);
        System.out.println(res);


    }
    static void dfs(int ca,int cb,int cd,int fa,int fb,int fd){
        if(ca==fa&&cb==fb){

            return;
        }
        if(ca<=10&&cb<=10&&fa<=10&&fb<=10
                &&ca>0&&cb>0&&fa>0&&fb>0){
//            System.out.println(ca+":"+cb+"----"+fa+":"+fb);
            if(flg[ca][cb][cd][fa][fb][fd]){
                res=0;
                return;
            }
            flg[ca][cb][cd][fa][fb][fd]=true;
        }

        if(ca+xd[cd]>10||cb+yd[cd]>10||ca+xd[cd]<1||cb+yd[cd]<1||roads[ca+xd[cd]][cb+yd[cd]]=='*'){
            cd=(cd+1)%4;

        }else {
            ca=ca+xd[cd];
            cb=cb+yd[cd];
        }
        if(fa+xd[fd]>10||fb+yd[fd]>10||fa+xd[fd]<1||fb+yd[fd]<1||roads[fa+xd[fd]][fb+yd[fd]]=='*')
            fd=(fd+1)%4;
        else {
            fa=fa+xd[fd];
            fb=fb+yd[fd];
        }
        res++;
        dfs(ca,cb,cd,fa,fb,fd);


    }
}
