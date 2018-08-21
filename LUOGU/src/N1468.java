import java.util.Scanner;

public class N1468 {
    public static void main(String[] args) {
        /*
        * 值得注意的点：２^4＝１６种情况，怎么用循环的形式表示出来的
        *
        * */
//        似乎解决不来重复的问题
        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
        int c=scanner.nextInt();
        int[] open=new int[n+1];
        for(int i=1;i<=n;i++){
            open[i]=-1;
        }
        int x=scanner.nextInt();

        while (x!=-1){
            open[x]=1;
            x=scanner.nextInt();
        }
        x=scanner.nextInt();
        while (x!=-1){
            open[x]=0;
            x=scanner.nextInt();
        }
        int[][] states=new int[17][n+1];
        int cnt=0;
        for(int i=0;i<=1;i++){
            for(int j=0;j<=1;j++){
                for(int k=0;k<=1;k++){
                    for(int l=0;l<=1;l++){
                        if((i+j+k+l)%2==c%2&&(i+j+k+l<=c)){
                            cnt++;
                            for(int q=1;q<=n;q++){
                                states[cnt][q]=1;
                            }
                            if(i==1)
                                for(int q=1;q<=n;q++)
                                    states[cnt][q]=1-states[cnt][q];
                            if(j==1)
                                for(int q=1;q<=n;q=q+2)
                                    states[cnt][q]=1-states[cnt][q];
                            if(k==1)
                                for (int q=2;q<=n;q=q+2)
                                    states[cnt][q]=1-states[cnt][q];
                            if(l==1)
                                for (int q=1;q<=n;q=q+3)
                                    states[cnt][q]=1-states[cnt][q];
                            for(int q=1;q<=n;q++)
                                if(states[cnt][q]==open[q]||open[q]==-1);
                                else{
                                    cnt--;
                                    break;
                                }
                        }
                    }
                }
            }
        }
        if(cnt==0)
            System.out.println("IMPOSSIBLE");
        for(int l=1;l<=cnt;l++){
            for(int i=l+1;i<=cnt;i++){
                for(int j=1;j<=n;j++){
                    if(states[l][j]>states[i][j]){
                        for(int k=1;k<=n;k++){
                            int t=states[i][k];
                            states[i][k]=states[l][k];
                            states[l][k]=t;
                        }
                        break;
                    }else if(states[l][j]<states[i][j]){
                        break;
                    }
                }
            }
        }

        for(int i=1;i<=cnt;i++){
            for(int j=1;j<=n;j++){
                if(j==n)
                    System.out.println(states[i][j]);
                else
                    System.out.print(states[i][j]);
            }
        }


    }


}
