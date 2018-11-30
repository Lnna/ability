import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Permutation {
    private static int[] input;
    private static List<List<Integer>> res;
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int x=scanner.nextInt();
        input=new int[x];
        for(int i=0;i<x;i++){
            input[i]=scanner.nextInt();
        }
        res=new ArrayList<>();
        Permutation main=new Permutation();
        main.permute(input);
        for(int i=0;i<res.size();i++){
            System.out.println(res.get(i).toString());
        }
    }
    public List<List<Integer>> permute(int[] nums) {
        recur(nums,0);
        return res;
    }

    private void recur(int[] nums,int start){
        if(start==nums.length-1){
            List<Integer> list=new ArrayList<>();
            for(int i=0;i<nums.length;i++){
                list.add(Integer.valueOf(nums[i]));
            }
            res.add(list);
        }
        for(int i=start;i<nums.length;i++){
            boolean flg=true;
//            对于有重复的，直接到最后一个再计算，前面的都略过
            for(int j=1+i;j<nums.length;j++){
                if(nums[j]==nums[i]){
                    flg=false;
                    break;
                }
            }
            if(flg){
                int tmp=nums[i];
                nums[i]=nums[start];
                nums[start]=tmp;
                recur(nums,start+1);
                nums[start]=nums[i];
                nums[i]=tmp;
            }
        }
    }
}
