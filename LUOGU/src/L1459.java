
import java.util.*;

public class L1459 {
    /*
     * P1459
     * 思路：位置正确的搁置，位置互换刚好正确的先交换，再交换需要两步的。
     * 编程思路：
     * １．ｔｍｐ数组作为排好序的正确数组，用于比较
     * ２．先遍历一次，把刚好交换一次的交换
     * ３．再遍历一次，把剩下位置不正确的，找到正确值所在的位置，交换
     * */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] pride = new int[n];
        int[] other = new int[n];

        for (int i = 0; i < n; i++) {
            pride[i] = scanner.nextInt();
            other[i] = pride[i];
        }
        Arrays.sort(other);
        int change = 0;
        for (int i = 0; i < n; i++) {
            if (pride[i] != other[i]) {
                for (int j = 0; j < n; j++) {
                    if (pride[j] == other[i] && other[j] == pride[i]) {
                        change++;
                        pride[j] = pride[i];
                        pride[i] = other[i];
                        break;
                    }
                }
            }
        }
        for (int i = 0; i < n; i++) {
            if (pride[i] != other[i]) {
                for (int j = n - 1; j > i; j--) {

                    if (pride[j] == other[i]) {
                        change++;
                        pride[j] = pride[i];
                        pride[i] = other[i];
                        break;
                    }
                }
            }
        }
        System.out.println(change);


    }
}
