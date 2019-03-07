import java.util.ArrayList;
import java.util.List;

public class Leet313 {
    public static int nthSuperUglyNumber(int n, int[] primes) {
        List<Integer> list=new ArrayList<>();
        list.add(1);
        int pointer[] =new int[primes.length];

        while (list.size()<n){
            int mid=0,mv=Integer.MAX_VALUE;
            for(int j=0;j<pointer.length;j++){
                int tmp=list.get(pointer[j])*primes[j];
                if(tmp<mv){
                    mid=j;
                    mv=tmp;
                }
            }

            pointer[mid]++;
            if(list.get(list.size()-1)!=mv)
                list.add(mv);
        }
        return list.get(list.size()-1);

    }

    public static void main(String[] args) {
        int[] primes={2,7,13,19};
         nthSuperUglyNumber(12,primes);
    }
}
