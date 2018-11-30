import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class PermuSeq {
    private static List<List<Integer>> pers;
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
        int k=scanner.nextInt();
        pers=new ArrayList<>();
        System.out.println(getPermutation(n,k));
    }
    private static String getPermutation(int n,int k){
        int[] nums=new int[n];
        for (int i=0;i<n;i++){
            nums[i]=i+1;
        }
        String res="";

        if(k>1) {
            while (--k>0){
                nextPermutation(nums);
            }
        }
        for(int i=0;i<nums.length;i++){
            res+=nums[i];
        }
        return res;
    }
    public static void nextPermutation(int[] nums) {
        if(nums.length==1) return;
        for(int i=nums.length-2;i>=0;i--){
            if(nums[i]<nums[i+1]){
                int[] tmp=new int[nums.length-i-1];
                for(int j=i+1;j<nums.length;j++){
                    tmp[j-i-1]=nums[j];
                }
                Arrays.sort(tmp);
                for(int j=0;j<tmp.length;j++){
                    if(tmp[j]>nums[i]){
                        int t=tmp[j];
                        tmp[j]=nums[i];
                        nums[i]=t;
                        break;
                    }
                }
                for(int j=0;j<tmp.length;j++){
                    nums[i+j+1]=tmp[j];
                }
                break;
            }
            if(i==0){
                Arrays.sort(nums);
            }
        }
//        System.out.println(nums.toString());
    }

}
