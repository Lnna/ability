import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DP39 {
//    private static List<List<Integer>> lists=new ArrayList<>();
    public static void main(String[] args) {
        int[] cand={2,3,6,7};
        Arrays.sort(cand);
        combinationSum(cand,7);
    }
    public static List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> lists=new ArrayList<>();
        recur(lists,new ArrayList<>(),candidates,target,0);
        for (int i=0;i<lists.size();i++){
            System.out.println(lists.get(i).toString());
        }
        return lists;
    }
    private static void recur(List<List<Integer>> lists,List<Integer> list,int[] cand,int t,int s){
        if(t<0) return;
        if(t==0){
            lists.add(new ArrayList<>(list));
            return;
        }
        for(int i=s;i<cand.length;i++){
            list.add(cand[i]);
            recur(lists,list,cand,t-cand[i],i);
            list.remove(list.size()-1);
        }
    }

}
