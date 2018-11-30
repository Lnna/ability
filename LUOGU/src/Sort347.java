import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/*
* bucket sort:分桶排序
*
* */
public class Sort347 {
    public static void main(String[] args) {
        int[] nums={1,1,2,3,3,4,5,5,5};
        topKFrequent(nums,3);
    }
    public static List<Integer> topKFrequent(int[] nums, int k) {
        Map<Integer,Integer> map=new HashMap<>();
        for(int i=0;i<nums.length;i++){
            map.put(nums[i],map.getOrDefault(nums[i],0)+1);
        }
        List<Integer>[] lists=new List[nums.length+1];
        for(Integer key:map.keySet()){
            if(lists[map.get(key)]==null)
                lists[map.get(key)]=new ArrayList<>();
            lists[map.get(key)].add(key);
        }
        List<Integer> res=new ArrayList<>();
        for (int i=nums.length;i>0;i--){
            if(lists[i]!=null && lists[i].size()>0){
                if(k-lists[i].size()>=0){
                    res.addAll(lists[i]);
                    k=k-lists[i].size();
                }else {
                    for(int j=0;j<k;j++){
                        res.add(lists[i].get(j));

                    }
                    break;
                }
            }
        }
        System.out.println(res.toString());
        return res;

    }
}
