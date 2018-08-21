import java.util.Scanner;

public class L1470 {
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        String[] set=new String[200];
        String s=scanner.next();
        int n=0;
        while (!s.equals(".")){
            set[n++]=s;
            s=scanner.next();
        }
        scanner.nextLine();
        String str="";
//        String t=scanner.nextLine();
//        while (t!=null&&!t.equals("")){
//            str=str+t;
//            t=scanner.nextLine();
//        }
        while (scanner.hasNextLine()){
            str+=scanner.nextLine();
        }
        int len=str.length();
        boolean[] flg=new boolean[len];
        for(int i=0;i<n;i++){
            int sl=set[i].length();
            for(int j=0;j<=len-sl;j++){
                if(str.substring(j,j+sl).equals(set[i])){
                    for(int k=j;k<j+sl;k++){
                        if(!flg[k])
                            flg[k]=true;
                    }
                }
            }
        }
        int res=0;
        for(int i=0;i<len;i++){
            if(!flg[i]){
                res=i;
                break;
            }
            if(i==len-1)
                res=len;
        }
        System.out.println(res);

    }
}
