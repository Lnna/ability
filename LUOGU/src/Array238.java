public class Array238 {
    public static void main(String[] args) {
        int[] nums={1,2,3,4};
        productExceptSelf(nums);
    }
    /*
     * 先从左至右把该元素前面的都乘上，再从右向左，把该元素后面的都乘上
     *
     * */
    public static int[] productExceptSelf(int[] nums) {
        int[] res=new int[nums.length];
        int tmp=1;
        for(int i=0;i<nums.length;i++){
            res[i]=tmp;
            tmp*=nums[i];
        }
        tmp=1;
        for (int i=nums.length-1;i>=0;i--){
            res[i]*=tmp;
            tmp*=nums[i];
        }
        for (int i=0;i<res.length;i++){
            System.out.println(res[i]);
        }
        return res;
    }
}
