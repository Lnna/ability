import java.util.ArrayList;
import java.util.List;
import java.util.Stack;


class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}
/*
* 二叉树的遍历：迭代和递归方法；二叉查找树的判定
* */
public class BTIT94 {
    private static List<Integer> res;

    public static void main(String[] args) {
        TreeNode treeNode=new TreeNode(1);
        treeNode.left=null;
        treeNode.right=new TreeNode(2);
        treeNode.right.left=new TreeNode(3);
        treeNode.right.right=null;
        res=new ArrayList<>();
        inorderTraversal(treeNode);
    }

    public static List<Integer> inorderTraversal(TreeNode root) {
//        iteratively
        Stack<TreeNode> stack=new Stack<>();
        TreeNode tmp=root;
        while (stack.size()>0 || tmp!=null){
            while (tmp!=null){
                stack.push(tmp);
                tmp=tmp.left;
            }
            TreeNode t=stack.pop();
            res.add(t.val);
            tmp=t.right;

        }


        System.out.println(res.toString());
        return res;
    }
    /*
    * 二叉搜索树的判定：二叉查找树中序遍历结果是递增序列。
    * */
    public static void isValidBST(TreeNode root) {

        inorder(root);
        for (int i=1;i<res.size();i++){
            if(res.get(i)<=res.get(i-1)){
                System.out.println(false);
                break;
            }
            if(i==res.size()-1)
                System.out.println(true);
        }
    }
    /*
     * recursion
     * */
    private static void inorder(TreeNode root){
        if(root!=null){
            inorder(root.left);
            res.add(root.val);
            inorder(root.right);
        }

    }
}
