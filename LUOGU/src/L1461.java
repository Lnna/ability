import java.util.Scanner;

public class L1461 {
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
        int b=scanner.nextInt();
        int d=scanner.nextInt();
        int i=1,a=1;
        int[] res=new int[n+1];
        int max=1;
        while (i<=b){
            max=max*2;
            i++;
        }
        i=1;

//        方法一
        while (i<n){
            for(int k=0;k<i;k++){
                if(hanming(res[k],a)<d)
                    break;
                if(k==i-1){
                    res[i]=a;
                    i++;

                }

            }
            a++;


        }
        for(int m=0;m<i;m++){
            if(m>0&&m%10==0)
                System.out.println();
            System.out.print(res[m]+" ");
        }
    }
    static int  hanming(int a,int b){
        int k=a^b;
        int ans=0;
        while (k>0){
            ans+=k&1;
            k=k>>1;
        }
        return ans;
    }
}
