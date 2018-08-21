import java.util.Scanner;

public class L1457 {
    private static int N=0,M=0;
    private static int[][] wall;
    private static boolean[][][] room;
    private static int num=0;
    private static int max=0;
    private static boolean[][][] flg;
    private static int rooms=1;
    private static int[] nums;
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        N=scanner.nextInt();
        M=scanner.nextInt();
        wall=new int[M+1][N+1];
        for(int i=1;i<=M;i++){
            for(int j=1;j<=N;j++){
                wall[i][j]=scanner.nextInt();
            }
        }
        room=new boolean[M+1][N+1][4];
        for(int i=1;i<=M;i++){
            for(int j=1;j<=N;j++){
                if(wall[i][j]>=8){
                    wall[i][j]-=8;
                    room[i][j][3]=true;
                }
                if(wall[i][j]>=4){
                    wall[i][j]-=4;
                    room[i][j][2]=true;
                }
                if(wall[i][j]>=2){
                    wall[i][j]-=2;
                    room[i][j][0]=true;
                }
                if(wall[i][j]>=1){
                    wall[i][j]-=1;
                    room[i][j][1]=true;
                }
            }
        }

        nums=new int[M*N+1];
        flg=new boolean[M+1][N+1][4];
        for(int i=1;i<=M;i++){
            for(int j=1;j<=N;j++){
                if(wall[i][j]==0){
                    dfs(i,j);
                    nums[rooms]=num;
                    max=Math.max(max,num);
                    num=0;
                    rooms++;
                }

            }
        }
        int x=0,y=0,d=0,rm=0;
        for(int i=1;i<=M;i++){
            for(int j=N;j>0;j--){
                if(room[i][j][3]&&i+1<=M&&wall[i][j]!=wall[i+1][j]){
                    int tmp=nums[wall[i][j]]+nums[wall[i+1][j]];
                    if(rm<tmp||(rm==tmp&&(y>j||(y==j&&x<i)))){
                        x=i;y=j;d=3;rm=tmp;
                    }
                }
                if(room[i][j][1]&&j-1>0&&wall[i][j]!=wall[i][j-1]){
                    int tmp=nums[wall[i][j]]+nums[wall[i][j-1]];
                    if(rm<tmp||(rm==tmp&&(y>j||(y==j&&x<i)))){
                        x=i;y=j;d=1;rm=tmp;
                    }
                }

            }
        }

        System.out.println(rooms-1);
        System.out.println(max);
        System.out.println(rm);
        if(d==1){
            System.out.println(String.format("%d %d %s",x,y-1,"E" ));
        }
        if(d==3){
            System.out.println(String.format("%d %d %s",x+1,y,"N" ));
        }




    }
    static void dfs(int x,int y){
        if(x>M||x<1||y<1||y>N||wall[x][y]>0) return;
        wall[x][y]=rooms;
        num++;
        for(int out=0;out<4;out++){
            if(!flg[x][y][out]&&!room[x][y][out]){
                flg[x][y][out]=true;
                if(out==0){
                    x=x-1;
                    dfs(x,y);
                    x=x+1;
                }
                if(out==1){
                    y=y-1;
                    dfs(x,y);
                    y=y+1;
                }

                if(out==2) {
                    y = y + 1;
                    dfs(x,y);
                    y=y-1;
                }
                if(out==3) {
                    x = x + 1;
                    dfs(x,y);
                    x=x-1;
                }

            }
        }

    }
}
