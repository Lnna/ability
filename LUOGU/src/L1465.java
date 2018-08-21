import java.util.Scanner;

public class L1465 {
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int n=scanner.nextInt();
        char[] c={'I','V','X','L','C','D','M'};
        String[] r1={"","I","II","III","IV","V","VI","VII","VIII","XI"};
        String[] r10={"","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"};
        String[] r100={"","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"};
        String[] r1000={"","M","MM","MMM"};
        String[] rome=new String[3500];
        for(int i=1;i<3500;i++){
            if(i<10){
                rome[i]=r1[i];
            }else if(i<100){
                int ct=i/10;
                int m=i%10;
                if(m!=0)
                    rome[i]=r10[ct]+r1[m];
                else
                    rome[i]=r10[ct];
            }else if(i<1000){
                int ct=i/100;
                int m=i%100;
                if(m!=0)
                    rome[i]=r100[ct]+rome[m];
                else
                    rome[i]=r100[ct];
            }else {
                int ct=i/1000;
                int m=i%1000;
                if(m!=0)
                    rome[i]=r1000[ct]+rome[m];
                else
                    rome[i]=r1000[ct];
            }
        }
        int[] num=new int[7];
        for(int i=1;i<=n;i++){
            int j=rome[i].length();
            for(int k=0;k<j;k++){
                switch (rome[i].charAt(k)){
                    case 'I':
                        num[0]+=1;
                        break;
                    case 'V':
                        num[1]+=1;
                        break;
                    case 'X':
                        num[2]+=1;
                        break;
                    case 'L':
                        num[3]+=1;
                        break;
                    case 'C':
                        num[4]+=1;
                        break;
                    case 'D':
                        num[5]+=1;
                        break;
                    case 'M':
                        num[6]+=1;
                        break;
                    default:
                        continue;
                }
            }
        }
        int i=0;
        while (i<7&&num[i]>0){
            System.out.println(c[i]+" "+num[i]);
            i++;
        }
//        for(int k=1;k<=n;k++){
//            System.out.print(rome[k]+" ");
//        }
    }

}
