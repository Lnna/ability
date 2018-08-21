import java.util.Scanner;

public class L1467 {
    private static int flg[];
    private static int res=0;
    private static int st=0;
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int m=scanner.nextInt();
        while (res==0){
            m++;
            flg=new int[10];
            st=0;
            if(dup(m)){
                flg[st]=2;
                if(move(m,st)){
                    res=m;
                    System.out.println(res);
                    return;
                }

            }
        }
    }
    static int bits(int x){
        int b=1;
        while (x>0){
            x=x/10;
            b=b*10;
        }
        b=b/10;
        return b;
    }
    static boolean dup(int x){
        int a=0;
        while (x!=0){
            a=x%10;
            if(a==0||flg[a]>0)
                return false;
            else
                flg[a]=1;
            st=x;
            x=x/10;
        }
        return true;
    }
    static boolean move(int x,int n){
        int b=bits(x);
        for(int i=0;i<n;i++){
            int q=x/b;
            x=x%b;
            x=x*10+q;
        }
        b=bits(x);
        n=x/b;
        for(int i=1;i<10;i++){
            if(flg[i]==1) break;
            if(i==9&&n==st)
                return true;
        }
        if(flg[n]>1)
            return false;
        else {
            flg[n]=2;
            return move(x,n);
        }
    }


}
