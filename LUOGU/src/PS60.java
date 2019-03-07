public class PS60 {
    private static int sk=0;
    private static boolean[] flg;
    private static String res="";

    public static void main(String[] args) {
        int n=3;
        int k=3;
        System.out.println(getPermutation(n,k));
    }
    public static String getPermutation(int n, int k) {
        sk=k;
        flg=new boolean[n+1];
        return recur(n,"");
    }
    private static String recur(int n,String s){
        if(s.length()==n){
            if(sk==1){
                res=s;
                return res;
            }else{
                sk--;
                return "";
            }
        }
        for(int i=1;i<=n;i++){
            if(flg[i])
                continue;
            flg[i]=true;
            s=s+i;
            if(!recur(n,s).equals(""))
                return res;
            else{
                s=s.substring(0,s.length()-1);
                flg[i]=false;
            }

        }
        return "";
    }
}
