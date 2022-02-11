package Project;

public class AVLTree {
	protected AVLNode root;
	int height;

	public AVLTree() {
		root = null;
	}

	int height(AVLNode N) {
		if (N == null)
			return 0;

		return N.height;
	}

	AVLNode rightRotate(AVLNode t) {
		AVLNode x = t.leftChild;
		AVLNode T2 = x.rightChild;

		x.rightChild = t;
		t.leftChild = T2;

		t.height = Math.max(height(t.leftChild), height(t.rightChild)) + 1;
		x.height = Math.max(height(x.leftChild), height(x.rightChild)) + 1;

		return x;
	}

	AVLNode leftRotate(AVLNode x) {
		AVLNode y = x.rightChild;
		AVLNode T2 = y.leftChild;

		y.leftChild = x;
		x.rightChild = T2;

		x.height = Math.max(height(x.leftChild), height(x.rightChild)) + 1;
		y.height = Math.max(height(y.leftChild), height(y.rightChild)) + 1;
		return y;
	}

	int getBalance(AVLNode N) {
		if (N == null)
			return 0;
		return height(N.leftChild) - height(N.rightChild);
	}

	AVLNode insert(String word, AVLNode t) {
		if (t == null) {
			t = new AVLNode(word);
			System.out.println("Added " + word);
		} else if (word.toLowerCase().compareTo(t.getWord().toLowerCase()) < 0)
			t.leftChild = insert(word, t.leftChild);
		else if (word.toLowerCase().compareTo(t.getWord().toLowerCase()) > 0)
			t.rightChild = insert(word, t.rightChild);
		else
			System.out.println(word + " is already in the dictionary");

		t.height = Math.max(height(t.leftChild), height(t.rightChild)) + 1;

		int balance = getBalance(t);

		// RL Case
		if (balance < -1 && word.toLowerCase().compareTo(t.rightChild.getWord().toLowerCase()) < 0) {
			t.rightChild = rightRotate(t.rightChild);
			return leftRotate(t);
		}

		// LR Case
		if (balance > 1 && word.toLowerCase().compareTo(t.leftChild.getWord().toLowerCase()) > 0) {
			t.leftChild = leftRotate(t.leftChild);
			return rightRotate(t);
		}

		// RR Case
		if (balance < -1 && word.toLowerCase().compareTo(t.getWord().toLowerCase()) > 0)
			return leftRotate(t);

		// LL Case
		if (balance > 1 && word.toLowerCase().compareTo(t.getWord().toLowerCase()) < 0)
			return rightRotate(t);

		return t;
	}

	boolean isContains(String word, AVLNode t) {
		if (Search(word, t) != null)
			return true;
		return false;

	}

	AVLNode Search(String word, AVLNode t) {
		if (t == null) {
			return null;
		}
		if (word.toLowerCase().equals(t.getWord().toLowerCase())) {
			return t;
		} else if (word.toLowerCase().compareTo(t.getWord().toLowerCase()) < 0) {
			return Search(word, t.leftChild);
		} else if (word.toLowerCase().compareTo(t.getWord().toLowerCase()) > 0) {
			return Search(word, t.rightChild);
		} else
			return null;

	}

	AVLNode minValueNode(AVLNode node) {
		AVLNode current = node;

		/* loop down to find the leftmost leaf */
		while (current.leftChild != null)
			current = current.leftChild;

		return current;
	}

	AVLNode deleteNode(String word, AVLNode root) {

		if (root == null)
			return root;
		if (word.toLowerCase().compareTo(root.getWord().toLowerCase()) < 0)
			root.leftChild = deleteNode(word, root.leftChild);
		else if (word.toLowerCase().compareTo(root.getWord().toLowerCase()) > 0)
			root.rightChild = deleteNode(word, root.rightChild);

		else {
			if ((root.leftChild == null) || (root.rightChild == null)) {
				AVLNode temp = null;
				if (temp == root.leftChild)
					temp = root.rightChild;
				else
					temp = root.leftChild;

				// No child case
				if (temp == null) {
					temp = root;
					root = null;
				} else
					root = temp;

			} else {
				AVLNode temp = minValueNode(root.rightChild);
				root.setWord(temp.getWord());

				root.rightChild = deleteNode(temp.getWord(), root.rightChild);
			}
		}

		if (root == null)
			return root;

		root.height = Math.max(height(root.leftChild), height(root.rightChild)) + 1;

		int balance = getBalance(root);

		// Right Left Case
		if (balance < -1 && getBalance(root.rightChild) > 0) {
			root.rightChild = rightRotate(root.rightChild);
			return leftRotate(root);
		}
		// Left Right Case
		if (balance > 1 && getBalance(root.leftChild) < 0) {
			root.leftChild = leftRotate(root.leftChild);
			return rightRotate(root);
		}
		// Left Left Case
		if (balance > 1 && getBalance(root.leftChild) >= 0)
			return rightRotate(root);
		// Right Right Case
		if (balance < -1 && getBalance(root.rightChild) <= 0)
			return leftRotate(root);

		return root;
	}

	void preorder(AVLNode t) {
		if (t == null) {
			return;
		}
		System.out.print(" " + t.getWord());
		preorder(t.leftChild);
		preorder(t.rightChild);
	}

	void inorder(AVLNode t) {
		if (t == null) {
			return;
		}
		inorder(t.leftChild);
		System.out.print("-" + t.getWord());
		inorder(t.rightChild);
	}

	void postorder(AVLNode t) {
		if (t == null) {
			return;
		}
		postorder(t.leftChild);
		postorder(t.rightChild);
		System.out.print(" " + t.getWord());
	}

	void levelorder(AVLNode t) {
		int x = height(root);
		int j;
		for (j = 1; j <= x; j++)
			givenLevel(root, j);
		System.out.println();
	}

	int Height(AVLNode root) {
		if (root == null)
			return 0;
		else {
			int leftHeight = height(root.leftChild);
			int rightHeight = height(root.rightChild);

			if (leftHeight > rightHeight)
				return (leftHeight + 1);
			else
				return (rightHeight + 1);
		}
	}

	void givenLevel(AVLNode root, int level) {
		if (root == null)
			return;
		if (level == 1)
			System.out.print(" " + root.getWord());

		else if (level > 1) {
			givenLevel(root.leftChild, level - 1);
			givenLevel(root.rightChild, level - 1);
		}
	}
}
