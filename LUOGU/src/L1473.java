import java.util.Scanner;

public class L1473 {
    private static int n;
    private static String signal="";
    private static int num=0;
    private static String[] res;
    private static char[] op={' ','+','-'};
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        n=scanner.nextInt();
        res=new String[1000000];
        signal+=1;
        dfs(2);
        for(int i=0;i<num;i++){
            System.out.println(res[i]);
        }

    }
    static void dfs(int x){
        if(x>n){
            int tmp=0;
            String[] s1=signal.replaceAll(" ","").split("[+-]");
//            System.out.println("signal:"+signal);
            String s2=signal.replaceAll(" ","").replaceAll("[1-9]","");
//            System.out.println("s2:"+s2);
            tmp+=Integer.valueOf(s1[0]);
            for(int i=0;i<s2.length();i++){
                if(s2.charAt(i)=='+'){
                    tmp+=Integer.valueOf(s1[i+1]);
                }else {
                    tmp-=Integer.valueOf(s1[i+1]);
                }
            }
            if(tmp==0){
                res[num]=signal;
                num++;
            }
            return;
        }
        for(int i=0;i<3;i++){
            signal+=op[i]+""+x;
            dfs(x+1);
            signal=signal.substring(0,signal.length()-2);
        }
    }
}
