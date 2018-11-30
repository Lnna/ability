import java.util.ArrayList;
import java.util.List;

public class Number17 {
    private static char[][] lettersByDigits = new char[][]{{}, {'*'}, {'a', 'b', 'c'}, {'d', 'e', 'f'}, {'g', 'h', 'i'},
            {'j', 'k', 'l'}, {'m', 'n', 'o'}, {'p', 'q', 'r', 's'}, {'t', 'u', 'v'}, {'w', 'x', 'y', 'z'}};
    private static String input="";
    private static List<String> res;
    public static void main(String[] args) {
        letterCombinations("");
    }
    public static List<String> letterCombinations(String digits) {
        res=new ArrayList<>();
//        input=digits;
//        recur("",0);
//        iteration
        for(int i=0;i<digits.length();i++){
            List<String> list=new ArrayList<>();
            char[] chars=lettersByDigits[digits.charAt(i)-'0'];
            for(String s:res){
                for(int j=0;j<chars.length;j++){
                    list.add(s+chars[j]);
                }
            }
            if(res.size()==0){
                for(int j=0;j<chars.length;j++){
                    list.add(""+chars[j]);
                }
            }
            res=list;

        }
        System.out.println(res.toString());
        return res;
    }

    private static void recur(String s,int n){
        if(n==input.length()){
            if(!s.equals(""))
                res.add(s);
            return;
        }
        for(int i=0;i<lettersByDigits[input.charAt(n)-'0'].length;i++){
            s+=lettersByDigits[input.charAt(n)-'0'][i];
            recur(s,n+1);
            s=s.substring(0,s.length()-1);
        }
    }
}
