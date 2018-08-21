import java.util.*;

public class L1458 {
    /*
     * P1458
     * */

    public static void main(String[] args) {

        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
//        double[] value=new double[n*n];
//        String[] s=new String[n*n];
        Map<String,Double> map=new HashMap<>();


//        int ct=0;
        for(int i=1;i<=n;i++){
            for(int j=0;j<i;j++){
                if(CoPrime(j,i)){
//                    value[ct]=(double)(j/i);
//                    s[ct]=j+"/"+i;
                    map.put(j+"/"+i,(double)j/i);
//                    ct++;
                }
            }
        }
        List<Map.Entry<String,Double>> list=new ArrayList<>(map.entrySet());
        Collections.sort(list, new Comparator<Map.Entry<String, Double>>() {
            @Override
            public int compare(Map.Entry<String, Double> o1, Map.Entry<String, Double> o2) {
                return o1.getValue().compareTo(o2.getValue());
            }
        });
        for(int i=0;i<list.size();i++){
            System.out.println(list.get(i).getKey());
        }
        System.out.println("1/1");

    }
    static boolean CoPrime(int a,int b){
        if(a==0&&b==1) return true;
        if(a==0) return false;
        for(int i=2;i<=a;i++){
            if(b%i==0&&a%i==0)
                return false;
        }
        return true;
    }

}
