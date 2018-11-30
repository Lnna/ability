import java.util.Arrays;

public class NextPermu {
    public static void main(String[] args) {
        int[] nums={1,1,5,2};
        nextPermutation(nums);
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
