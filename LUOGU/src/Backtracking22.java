import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

public class Backtracking22 {
    private static char[] p;
    private static List<String> res;
    public static void main(String[] args) {
        generateParenthesis(4);
    }
    public static List<String> generateParenthesis(int n) {
        p=new char[n*2];
        res=new ArrayList<>();
        for(int i=0;i<n;i++){
            p[i]='(';
            p[i+n]=')';
        }
        recur(p,0);
        for(int i=0;i<res.size();i++){
            System.out.println(res.get(i));
        }
        return res;

    }
    private static void recur(char[] s,int start){
        if(start==s.length-1){
            if(judge(s)){
                String st="";
                for(int i=0;i<s.length;i++){
                    st+=s[i];
                }
                res.add(st);
            }
        }
        for(int i=start;i<s.length;i++){
            boolean flg=true;
            for(int j=1+i;j<s.length;j++){
                if(s[j]==s[i]){
                    flg=false;
                    break;
                }
            }
            if (flg){
                char tmp=s[start];
                s[start]=s[i];
                s[i]=tmp;
                recur(s,start+1);
                s[i]=s[start];
                s[start]=tmp;
            }
        }
    }
    private static boolean judge(char[] s){
        Stack<Character> stack=new Stack<>();
        for(int i=0;i<s.length;i++){
            if(s[i]=='('){
                stack.push(s[i]);
            }
            else if(stack.size()>0){
                    char c=stack.peek();
                    if(c=='(')
                        stack.pop();
                    else
                        return false;
            }else{
                return false;
            }
        }
        return true;

    }
}

